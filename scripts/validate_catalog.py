#!/usr/bin/env python3
"""Validate the public CardPilot catalog snapshot without third-party packages."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

BANKS = {"hsbc", "bochk", "bea"}
IMAGES = {
    "hsbc-student.jpg", "hsbc-pulse.png", "hsbc-mastercard-debit.jpg",
    "bochk-chill-platinum.png", "bochk-go-diamond.png", "bochk-go-platinum.png",
    "bochk-gba-youth.png", "bea-hku-student.png", "bea-udc-diamond.png",
}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VERSION = re.compile(r"^[1-9]\d{0,17}$")
PRIVATE_KEYS = {
    "lastFour", "cardNumber", "cvv", "expiry", "password", "token", "secret",
    "email", "phone", "transactions", "ledger", "accountNumber", "cardholder",
    "cardOverride", "welcomeTracking",
}


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


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_catalog.py docs/catalog.json")
    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), "root must be an object")
    check_unknown_keys(data, {"schemaVersion", "contentVersion", "publishedAt", "products"}, "root")
    require(data.get("schemaVersion") == 1, "schemaVersion must be 1")
    version = data.get("contentVersion")
    require(isinstance(version, int) and not isinstance(version, bool) and 0 < version < 10**18,
            "contentVersion must be a positive integer")
    parse_date(data.get("publishedAt"), "publishedAt")
    products = data.get("products")
    require(isinstance(products, list) and 1 <= len(products) <= 20, "products must have 1-20 items")
    require(IMAGES and BANKS, "internal image/bank set missing")
    seen: set[str] = set()
    for index, product in enumerate(products):
        require(isinstance(product, dict), f"products[{index}] must be an object")
        check_unknown_keys(product, {"id", "bankID", "imageResource", "baseRewardVerified", "welcomePlans", "catalog"},
                          f"products[{index}]")
        product_id = product.get("id")
        require(isinstance(product_id, str) and product_id and product_id not in seen,
                f"products[{index}].id must be unique and non-empty")
        seen.add(product_id)
        require(product.get("bankID") in BANKS, f"{product_id}: unknown bankID")
        require(product.get("imageResource") in IMAGES, f"{product_id}: imageResource must be bundled")
        require(isinstance(product.get("baseRewardVerified"), bool), f"{product_id}: baseRewardVerified must be bool")
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
            require(isinstance(rule, dict), f"{product_id}: rule must be an object")
            rule_id = rule.get("id")
            require(isinstance(rule_id, str) and rule_id and rule_id not in rule_ids,
                    f"{product_id}: duplicate or empty rule id")
            rule_ids.add(rule_id)
            require(rule.get("kind") in {"cashback", "welcome"}, f"{product_id}/{rule_id}: invalid kind")
            https(rule.get("sourceURL"), f"{product_id}/{rule_id}.sourceURL")
            parse_date(rule.get("startsOn"), f"{product_id}/{rule_id}.startsOn")
            parse_date(rule.get("endsOn"), f"{product_id}/{rule_id}.endsOn")
        plan_ids: set[str] = set()
        for plan in plans:
            require(isinstance(plan, dict), f"{product_id}: welcome plan must be an object")
            plan_id = plan.get("id")
            require(isinstance(plan_id, str) and plan_id and plan_id not in plan_ids,
                    f"{product_id}: duplicate or empty welcome plan id")
            plan_ids.add(plan_id)
            require(plan.get("kind") in {"main", "addon"}, f"{product_id}/{plan_id}: invalid plan kind")
            https(plan.get("sourceURL"), f"{product_id}/{plan_id}.sourceURL")
            for field in ("applicationStartsOn", "applicationEndsOn"):
                if plan.get(field) is not None:
                    parse_date(plan[field], f"{product_id}/{plan_id}.{field}")
            for rule_id in plan.get("ruleIDs", []):
                require(rule_id in rule_ids, f"{product_id}/{plan_id}: unknown rule {rule_id}")
    walk_keys(data)
    print(f"valid catalog: {len(products)} products, contentVersion {version}, publishedAt {data['publishedAt']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
