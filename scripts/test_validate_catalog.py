#!/usr/bin/env python3
"""Regression test for the public catalog's fixed card-artwork canvas."""

from __future__ import annotations

import hashlib
import copy
import json
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib
from pathlib import Path
from validate_catalog import validate_usage_guide

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
VALIDATOR = ROOT / "scripts" / "validate_catalog.py"


def png_1x1() -> bytes:
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    return b"".join([
        b"\x89PNG\r\n\x1a\n",
        chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)),
        chunk(b"IDAT", zlib.compress(b"\x00\x00\x00\x00")),
        chunk(b"IEND", b""),
    ])


class CardArtworkValidationTests(unittest.TestCase):
    def test_rejects_merchant_keyword_arrays_before_clients_decode_them(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "docs"
            shutil.copytree(DOCS, target)
            catalog_path = target / "catalog.json"
            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            catalog["products"][0]["catalog"]["rules"][0]["merchantKeywords"] = ["Example shop"]
            catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(catalog_path)],
                capture_output=True, text=True, check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("merchantKeywords must be a comma-separated string", result.stdout + result.stderr)

    def test_allows_bank_and_card_images_to_be_added_later(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "docs"
            shutil.copytree(DOCS, target)
            catalog_path = target / "catalog.json"
            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            catalog["banks"][0]["logo"] = None
            catalog["products"][0]["artwork"] = None
            catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(catalog_path)],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_a_card_that_is_not_1200x756(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "docs"
            shutil.copytree(DOCS, target)
            catalog_path = target / "catalog.json"
            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            product = catalog["products"][0]
            image_path = target / "images" / "cards" / "not-1200.png"
            payload = png_1x1()
            image_path.write_bytes(payload)
            product["artwork"] = {
                "path": "images/cards/not-1200.png",
                "sha256": hashlib.sha256(payload).hexdigest(),
                "contentType": "image/png",
            }
            catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(catalog_path)],
                capture_output=True,
                text=True,
                check=False,
            )
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0, output)
            self.assertIn("card artwork must be 1200x756", output)


class UsageGuideValidationTests(unittest.TestCase):
    def example(self) -> dict:
        text = (DOCS / "usage-guide.md").read_text(encoding="utf-8")
        return json.loads(re.search(r"```json\n(.*?)\n```", text, re.S).group(1))

    def test_documented_template_matches_contract_and_optional_fields(self) -> None:
        guide = self.example()
        validate_usage_guide(guide, "usageGuide", {"example.offer.monthly"})
        validate_usage_guide(None, "usageGuide", set())
        for key in ("capNote", "stopAfter", "warnings", "startsOn", "endsOn"):
            del guide["scenarios"][0][key]
        guide["scenarios"][0]["relatedOfferIDs"] = []
        validate_usage_guide(guide, "usageGuide", set())

    def test_product_level_guide_is_accepted_by_full_snapshot_validator(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "docs"
            shutil.copytree(DOCS, target)
            path = target / "catalog.json"
            catalog = json.loads(path.read_text(encoding="utf-8"))
            guide = self.example()
            guide["scenarios"][0]["relatedOfferIDs"] = [catalog["products"][0]["catalog"]["rules"][0]["id"]]
            catalog["products"][0]["usageGuide"] = guide
            path.write_text(json.dumps(catalog, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run([sys.executable, str(VALIDATOR), str(path)],
                                    capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_invalid_or_untraceable_scenarios(self) -> None:
        cases = {
            "unknown field": ("stopAmount", 2000),
            "wrong type": ("stopAfter", 2000),
            "empty text": ("title", "  "),
            "overlong": ("howToUse", "x" * 1201),
            "cross-card reference": ("relatedOfferIDs", ["other.card.offer"]),
            "duplicate references": ("relatedOfferIDs", ["example.offer.monthly"] * 2),
            "missing sources": ("sourceURLs", []),
            "insecure source": ("sourceURLs", ["http://example.com/terms"]),
            "credentials": ("sourceURLs", ["https://secret@example.com/terms"]),
            "invalid date": ("endsOn", "2026-02-30"),
        }
        for name, (field, value) in cases.items():
            with self.subTest(name=name):
                guide = self.example()
                guide["scenarios"][0][field] = value
                with self.assertRaises(SystemExit):
                    validate_usage_guide(guide, "usageGuide", {"example.offer.monthly"})
        for name in ("duplicate scenarios", "empty scenarios", "invalid range", "invalid review date"):
            with self.subTest(name=name):
                guide = self.example()
                if name == "duplicate scenarios":
                    guide["scenarios"].append(copy.deepcopy(guide["scenarios"][0]))
                elif name == "empty scenarios":
                    guide["scenarios"] = []
                elif name == "invalid range":
                    guide["scenarios"][0].update(startsOn="2026-12-01", endsOn="2026-10-01")
                else:
                    guide["reviewedOn"] = "2026-02-30"
                with self.assertRaises(SystemExit):
                    validate_usage_guide(guide, "usageGuide", {"example.offer.monthly"})


if __name__ == "__main__":
    unittest.main()
