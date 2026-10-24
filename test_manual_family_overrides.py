"""Test isolati per lo spostamento manuale delle famiglie."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import manual_family_overrides as m


class ManualFamilyOverridesTests(unittest.TestCase):
    def test_listing_id(self):
        url = "https://www.subito.it/fotografia/dji-cosmo-poket-rovigo-665258336.htm"
        self.assertEqual(m.listing_id(url), "665258336")
        self.assertIsNone(m.listing_id("https://example.org/"))

    def test_save_replace_and_remove(self):
        url = "https://www.subito.it/fotografia/dji-cosmo-poket-rovigo-665258336.htm"
        with tempfile.TemporaryDirectory() as tempdir:
            with patch.object(m, "DATABASE_PATH", Path(tempdir) / "manual.sqlite"):
                m.save_override(url, "DJI Osmo Pocket 3")
                self.assertEqual(m.get_overrides()["665258336"], "DJI Osmo Pocket 3")
                m.save_override(url, "DJI Osmo Pocket 2")
                self.assertEqual(m.get_overrides()["665258336"], "DJI Osmo Pocket 2")
                m.delete_override(url)
                self.assertEqual(m.get_overrides(), {})

    def test_bulk_save_is_atomic(self):
        urls = [
            "https://www.subito.it/videogiochi/xbox-console-659976708.htm",
            "https://www.subito.it/videogiochi/xbox-setie-s-659257097.htm",
        ]
        with tempfile.TemporaryDirectory() as tempdir:
            with patch.object(m, "DATABASE_PATH", Path(tempdir) / "manual.sqlite"):
                self.assertEqual(m.save_overrides(urls, "Xbox Series S"), 2)
                self.assertEqual(m.get_overrides(), {
                    "659976708": "Xbox Series S",
                    "659257097": "Xbox Series S",
                })
                with self.assertRaises(ValueError):
                    m.save_overrides(urls + ["not-a-subito-url"], "Xbox Series X")
                self.assertEqual(m.get_overrides()["659976708"], "Xbox Series S")

    def test_empty_family_is_rejected(self):
        with self.assertRaises(ValueError):
            m.save_override("https://www.subito.it/fotografia/prodotto-665258336.htm", "")

    def test_password_required(self):
        with patch.dict("os.environ", {}, clear=True):
            self.assertFalse(m.editor_authorized(""))
            self.assertFalse(m.editor_authorized("anything"))
        with patch.dict("os.environ", {"SUBITO_EDITOR_PASSWORD": "secret"}):
            self.assertFalse(m.editor_authorized("wrong"))
            self.assertTrue(m.editor_authorized("secret"))


if __name__ == "__main__":
    unittest.main()
