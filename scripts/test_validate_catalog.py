#!/usr/bin/env python3
"""Regression test for the public catalog's fixed card-artwork canvas."""

from __future__ import annotations

import hashlib
import json
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
