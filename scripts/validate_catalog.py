#!/usr/bin/env python3
"""Validate the public CardPilot Catalog V2 snapshot without third-party packages."""

from __future__ import annotations

import hashlib
import json
import re
import struct
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
BANK_ID = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
PRODUCT_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
HASH = re.compile(r"^[0-9a-f]{64}$")
ASSET_PATH = re.compile(r"^images/(banks|cards)/[A-Za-z0-9._-]+$")
PRIVATE_KEYS = {
    "lastFour", "cardNumber", "cvv", "expiry", "password", "token", "secret",
    "email", "phone", "transactions", "ledger", "accountNumber", "cardholder",
    "cardOverride", "welcomeTracking",
}
MAX_IMAGE_BYTES = 4_000_000
CARD_IMAGE_WIDTH = 1200
CARD_IMAGE_HEIGHT = 756
PAYMENT_METHODS = {
    "待确认", "Apple Pay", "实体卡", "网上支付", "支付宝", "微信支付",
    "UnionPay", "BoC Pay", "Huawei Pay", "PayMe",
}
RULE_KEYS = {
    "id", "name", "kind", "group", "startsOn", "endsOn", "sourceURL", "ratePercent",
    "capHKD", "capPeriod", "sharedCapGroup", "thresholdHKD", "bonusHKD", "minimumHKD",
    "monthlyPhysicalThresholdHKD", "channelCondition", "category", "currency",
    "paymentMethod", "merchantKeywords", "requiresPersonalDates", "enabled", "notes",
    "calculation",
}


def validate_payment_method(value: object, label: str) -> None:
    require(isinstance(value, str) and value in PAYMENT_METHODS,
            f"{label} must be one of {sorted(PAYMENT_METHODS)}; use UnionPay for all UnionPay labels")
MAX_IMAGE_DIMENSION = 2400


def fail(message: str) -> None:
    raise SystemExit(f"invalid catalog: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def parse_date(value: object, label: str) -> None:
    require(isinstance(value, str) and bool(DATE.fullmatch(value)), f"{label} must be YYYY-MM-DD")
    try:
        date.fromisoformat(value)
    except ValueError:
        fail(f"{label} is not a valid date: {value!r}")


def https(value: object, label: str) -> None:
    require(isinstance(value, str), f"{label} must be a string")
    parsed = urlparse(value)
    require(parsed.scheme == "https" and bool(parsed.netloc) and not parsed.username and not parsed.password,
            f"{label} must be an HTTPS URL without credentials")


def check_unknown_keys(value: dict, allowed: set[str], label: str) -> None:
    unknown = set(value) - allowed
    require(not unknown, f"{label} has unsupported fields: {sorted(unknown)}")


def walk_keys(value: object, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            require(key not in PRIVATE_KEYS, f"{path} contains private field {key!r}")
            walk_keys(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            walk_keys(item, f"{path}[{index}]")


def image_dimensions(data: bytes) -> tuple[str, int, int]:
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24 and data[12:16] == b"IHDR":
        return "image/png", struct.unpack(">II", data[16:24])[0], struct.unpack(">II", data[16:24])[1]
    if data.startswith(b"\xff\xd8"):
        index = 2
        while index + 9 < len(data):
            if data[index] != 0xFF:
                index += 1
                continue
            marker = data[index + 1]
            index += 2
            if marker in (0xD8, 0xD9):
                continue
            length = struct.unpack(">H", data[index:index + 2])[0]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                height, width = struct.unpack(">HH", data[index + 3:index + 7])
                return "image/jpeg", width, height
            index += length
        return "image/jpeg", 0, 0
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        chunk = data[12:16]
        if chunk == b"VP8X" and len(data) >= 30:
            width = int.from_bytes(data[24:27], "little") + 1
            height = int.from_bytes(data[27:30], "little") + 1
            return "image/webp", width, height
        if chunk == b"VP8 " and len(data) >= 30 and data[23:26] == b"\x9d\x01\x2a":
            return "image/webp", struct.unpack("<H", data[26:28])[0] & 0x3FFF, struct.unpack("<H", data[28:30])[0] & 0x3FFF
        if chunk == b"VP8L" and len(data) >= 25 and data[20] == 0x2F:
            bits = int.from_bytes(data[21:25], "little")
            return "image/webp", (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
        return "image/webp", 0, 0
    return "", 0, 0


def validate_asset(value: object, label: str, root: Path, folder: str) -> None:
    require(isinstance(value, dict), f"{label} must be an object")
    check_unknown_keys(value, {"path", "sha256", "contentType"}, label)
    path = value.get("path")
    require(isinstance(path, str) and bool(ASSET_PATH.fullmatch(path)) and path.startswith(f"images/{folder}/"),
            f"{label}.path must stay under images/{folder}/")
    require(".." not in Path(path).parts and not path.startswith("/"), f"{label}.path is unsafe")
    digest = value.get("sha256")
    require(isinstance(digest, str) and bool(HASH.fullmatch(digest)), f"{label}.sha256 must be lowercase SHA-256")
    content_type = value.get("contentType")
    require(content_type in {"image/png", "image/jpeg", "image/webp"}, f"{label}.contentType is unsupported")
    file = root / path
    require(file.is_file(), f"{label}: missing image {path}")
    require(file.stat().st_size <= MAX_IMAGE_BYTES, f"{label}: image exceeds {MAX_IMAGE_BYTES} bytes")
    payload = file.read_bytes()
    require(hashlib.sha256(payload).hexdigest() == digest, f"{label}: SHA-256 mismatch for {path}")
    actual_type, width, height = image_dimensions(payload)
    require(actual_type == content_type, f"{label}: file is {actual_type or 'unknown'}, expected {content_type}")
    require(0 < width <= MAX_IMAGE_DIMENSION and 0 < height <= MAX_IMAGE_DIMENSION,
            f"{label}: image dimensions must be 1...{MAX_IMAGE_DIMENSION}px")
    if folder == "cards":
        require(width == CARD_IMAGE_WIDTH and height == CARD_IMAGE_HEIGHT,
                f"{label}: card artwork must be {CARD_IMAGE_WIDTH}x{CARD_IMAGE_HEIGHT}px, got {width}x{height}px")


def validate_plan(plan: object, label: str, rule_ids: set[str]) -> str:
    require(isinstance(plan, dict), f"{label} must be an object")
    check_unknown_keys(plan, {
        "id", "title", "details", "sourceURL", "ruleIDs", "applicationChannels",
        "verified", "calculable", "periodType", "periodCount", "applicationStartsOn",
        "applicationEndsOn", "kind", "exclusionGroup",
    }, label)
    plan_id = plan.get("id")
    require(isinstance(plan_id, str) and bool(plan_id), f"{label}.id must be non-empty")
    require(plan.get("kind") in {"main", "addon"}, f"{label}.kind must be main or addon")
    https(plan.get("sourceURL"), f"{label}.sourceURL")
    for field in ("applicationStartsOn", "applicationEndsOn"):
        if plan.get(field) is not None:
            parse_date(plan[field], f"{label}.{field}")
    for rule_id in plan.get("ruleIDs", []):
        require(rule_id in rule_ids, f"{label}: unknown rule {rule_id}")
    return plan_id


def validate_rule(rule: object, label: str, seen: set[str]) -> None:
    require(isinstance(rule, dict), f"{label} must be an object")
    check_unknown_keys(rule, RULE_KEYS, label)
    rule_id = rule.get("id")
    require(isinstance(rule_id, str) and bool(rule_id) and rule_id not in seen, f"{label}: duplicate or empty rule id")
    seen.add(rule_id)
    require(rule.get("kind") in {"cashback", "welcome"}, f"{label}/{rule_id}: invalid kind")
    require(rule.get("group") in {"daily", "limited", "merchant", "welcome"},
            f"{label}/{rule_id}: explicit group is required")
    https(rule.get("sourceURL"), f"{label}/{rule_id}.sourceURL")
    for field in ("startsOn", "endsOn"):
        if rule.get(field) is not None:
            parse_date(rule[field], f"{label}/{rule_id}.{field}")
    if rule.get("paymentMethod") not in (None, ""):
        validate_payment_method(rule["paymentMethod"], f"{label}/{rule_id}.paymentMethod")
    calculation = rule.get("calculation")
    if isinstance(calculation, dict):
        for field in ("paymentMethods", "excludedPaymentMethods"):
            values = calculation.get(field, [])
            require(isinstance(values, list), f"{label}/{rule_id}.{field} must be an array")
            for value in values:
                validate_payment_method(value, f"{label}/{rule_id}.{field}[]")


def main() -> int:
    args = sys.argv[1:]
    base_path: Path | None = None
    if "--base" in args:
        index = args.index("--base")
        require(index + 1 < len(args), "--base requires a catalog path")
        base_path = Path(args[index + 1])
        del args[index:index + 2]
    if len(args) != 1:
        raise SystemExit("usage: validate_catalog.py docs/catalog.json [--base path/to/main/catalog.json]")
    path = Path(args[0])
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), "root must be an object")
    check_unknown_keys(data, {"schemaVersion", "contentVersion", "publishedAt", "banks", "products"}, "root")
    require(data.get("schemaVersion") == 2, "schemaVersion must be 2")
    version = data.get("contentVersion")
    require(isinstance(version, int) and not isinstance(version, bool) and 0 < version < 10**18,
            "contentVersion must be a positive integer")
    parse_date(data.get("publishedAt"), "publishedAt")
    if base_path is not None and base_path.exists():
        base = json.loads(base_path.read_text(encoding="utf-8"))
        old = base.get("contentVersion")
        require(isinstance(old, int) and version > old,
                f"contentVersion must increase above {old}")

    banks = data.get("banks")
    require(isinstance(banks, list) and 1 <= len(banks) <= 200, "banks must have 1...200 items")
    seen_banks: set[str] = set()
    root = path.parent
    for index, bank in enumerate(banks):
        label = f"banks[{index}]"
        require(isinstance(bank, dict), f"{label} must be an object")
        check_unknown_keys(bank, {"id", "name", "shortName", "logo", "searchTerms"}, label)
        bank_id = bank.get("id")
        require(isinstance(bank_id, str) and bool(BANK_ID.fullmatch(bank_id)) and bank_id not in seen_banks,
                f"{label}.id must be unique and stable")
        seen_banks.add(bank_id)
        require(isinstance(bank.get("name"), str) and 0 < len(bank["name"]) <= 100, f"{label}.name is invalid")
        require(isinstance(bank.get("shortName"), str) and 0 < len(bank["shortName"]) <= 60, f"{label}.shortName is invalid")
        terms = bank.get("searchTerms", [])
        require(isinstance(terms, list) and len(terms) <= 20 and all(isinstance(x, str) and 0 < len(x) <= 40 for x in terms),
                f"{label}.searchTerms is invalid")
        validate_asset(bank.get("logo"), f"{label}.logo", root, "banks")

    products = data.get("products")
    require(isinstance(products, list) and 1 <= len(products) <= 1000, "products must have 1...1000 items")
    seen: set[str] = set()
    for index, product in enumerate(products):
        label = f"products[{index}]"
        require(isinstance(product, dict), f"{label} must be an object")
        check_unknown_keys(product, {"id", "bankID", "artwork", "baseRewardVerified", "welcomePlans", "catalog", "searchTerms"}, label)
        product_id = product.get("id")
        require(isinstance(product_id, str) and bool(PRODUCT_ID.fullmatch(product_id)) and product_id not in seen,
                f"{label}.id must be unique and stable")
        seen.add(product_id)
        require(product.get("bankID") in seen_banks, f"{product_id}: unknown bankID")
        require(isinstance(product.get("baseRewardVerified"), bool), f"{product_id}: baseRewardVerified must be bool")
        validate_asset(product.get("artwork"), f"{product_id}.artwork", root, "cards")
        terms = product.get("searchTerms", [])
        require(isinstance(terms, list) and len(terms) <= 20 and all(isinstance(x, str) and 0 < len(x) <= 40 for x in terms),
                f"{product_id}: searchTerms is invalid")
        plans = product.get("welcomePlans")
        require(isinstance(plans, list), f"{product_id}: welcomePlans must be an array")
        catalog = product.get("catalog")
        require(isinstance(catalog, dict), f"{product_id}: catalog must be an object")
        require(catalog.get("id") == product_id, f"{product_id}: catalog.id must match product id")
        require("imageURL" not in catalog and "imageBase64" not in catalog,
                f"{product_id}: catalog must not carry artwork")
        https(catalog.get("sourceURL"), f"{product_id}.catalog.sourceURL")
        parse_date(catalog.get("verifiedOn"), f"{product_id}.catalog.verifiedOn")
        rules = catalog.get("rules")
        require(isinstance(rules, list), f"{product_id}: catalog.rules must be an array")
        rule_ids: set[str] = set()
        for rule in rules:
            validate_rule(rule, product_id, rule_ids)
        plan_ids: set[str] = set()
        for plan in plans:
            plan_id = validate_plan(plan, f"{product_id}.welcomePlans[{len(plan_ids)}]", rule_ids)
            require(plan_id not in plan_ids, f"{product_id}: duplicate welcome plan id {plan_id}")
            plan_ids.add(plan_id)
    walk_keys(data)
    print(f"valid catalog V2: {len(banks)} banks, {len(products)} products, contentVersion {version}, publishedAt {data['publishedAt']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
