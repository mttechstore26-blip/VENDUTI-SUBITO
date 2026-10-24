"""Regression tests for category-scoped recovery of unidentified models."""
import unittest

from unknown_model_taxonomy import classify_unknown_model


class UnknownModelTaxonomyTests(unittest.TestCase):
    def check(self, title, category, expected):
        self.assertEqual(classify_unknown_model(title.lower(), category.lower()), expected)

    def test_distinct_models(self):
        samples = [
            ("canon eos2000d fotocamera", "fotografia", "Canon EOS 2000D"),
            ("nikon d 3100 obiettivo", "fotografia", "Nikon D3100"),
            ("insta 360 x 4", "fotografia", "Insta360 X4"),
            ("amd 6800xt sapphire nitro", "informatica", "GPU • Radeon RX 6800 XT"),
            ("thinkpad t470p", "lenovo", "Lenovo ThinkPad T470p"),
            ("de longhi rivelia", "elettrodomestici", "De'Longhi Rivelia"),
            ("dayson v15", "elettrodomestici", "Dyson V15"),
            ("vivo x200 fe", "telefonia", "Vivo X200 FE"),
            ("bticino axolute", "giardino e fai da te", "BTicino Axolute"),
            ("adidas f50 elite", "sport", "Adidas F50 Elite"),
            ("nuna base curv", "tutto per i bambini", "Nuna Base Curv"),
            ("acme e 444 002", "collezionismo", "Fermodellismo • ACME E444"),
            ("legion go z1 extreme", "console 400", "Handheld • Lenovo Legion Go Z1 Extreme"),
        ]
        for title, category, expected in samples:
            with self.subTest(title=title):
                self.check(title, category, expected)

    def test_no_unjustified_model_inference(self):
        samples = [
            ("console", "console 120 350"),
            ("bimby", "elettrodomestici"),
            ("iphone", "telefonia"),
            ("fotocamera", "fotografia"),
            ("champagne dom perignon 2013", "collezionismo"),
        ]
        for title, category in samples:
            with self.subTest(title=title):
                self.assertIsNone(classify_unknown_model(title, category))

    def test_scoped_to_category(self):
        self.assertIsNone(classify_unknown_model("de longhi rivelia", "sport"))
        self.assertIsNone(classify_unknown_model("canon eos2000d", "telefonia"))


if __name__ == "__main__":
    unittest.main()
