import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "b2b-ui-designer"
sys.path.insert(0, str(SKILL / "scripts"))
import blueprint as bp  # noqa: E402
import contrast as c  # noqa: E402
import tokens as tk  # noqa: E402

ACCENTS = [None, "#6366f1", "#ffd400", "#00a3ff", "#111111", "#ffffff", "#0f766e", "#e11d48", "rgb(16 185 129)", "hsl(30 90% 55%)"]


class Contrast(unittest.TestCase):
    def test_known_ratios(self):
        self.assertAlmostEqual(c.ratio("#000", "#fff"), 21.0, places=2)
        self.assertAlmostEqual(c.ratio("#fff", "#fff"), 1.0, places=2)
        self.assertAlmostEqual(c.ratio("#767676", "#fff"), 4.54, places=2)

    def test_formats(self):
        self.assertEqual(c.parse("#abc")[:3], (170.0, 187.0, 204.0))
        self.assertEqual(c.parse("rgb(10, 20, 30)")[:3], (10.0, 20.0, 30.0))
        self.assertAlmostEqual(c.parse("rgba(0 0 0 / 50%)")[3], 0.5)
        self.assertEqual(c.to_hex(c.parse("hsl(0 100% 50%)")), "#ff0000")
        with self.assertRaises(c.ColorError):
            c.parse("not-a-colour")

    def test_translucent_is_composited(self):
        self.assertLess(c.ratio("rgba(0,0,0,0.2)", "#fff"), 2)

    def test_adjust_to(self):
        for color, bg in (("#ffd400", "#ffffff"), ("#1e3a8a", "#0a0a0b"), ("#a3e635", "#ffffff")):
            fixed = c.adjust_to(color, bg, 4.5)
            self.assertGreaterEqual(c.ratio(fixed, bg), 4.5, (color, bg, fixed))


class Tokens(unittest.TestCase):
    def test_every_direction_and_accent_passes(self):
        for d in tk.DIRECTIONS:
            for a in ACCENTS:
                rows = tk.report(tk.build(d, a))
                bad = [r for r in rows if not r["pass"]]
                with self.subTest(direction=d, accent=a):
                    self.assertEqual(bad, [])

    def test_css_has_themes(self):
        css = tk.to_css(tk.build("modern-saas"))
        self.assertIn("prefers-color-scheme: dark", css)
        self.assertIn(':root[data-theme="dark"]', css)
        self.assertIn("color-scheme: light", css)
        self.assertIn("--space-16: 1rem", css)
        dev = tk.to_css(tk.build("developer"))
        self.assertIn("color-scheme: dark", dev.split("}")[0])
        self.assertNotIn("prefers-color-scheme", dev)

    def test_json_and_tailwind(self):
        t = json.loads(json.dumps(tk.build("editorial")))
        self.assertEqual(t["direction"], "editorial")
        self.assertIn("display=swap", t["font_url"])
        self.assertIn("module.exports", tk.to_tailwind(tk.build("enterprise")))

    def test_unknown_direction(self):
        with self.assertRaises(KeyError):
            tk.build("brutalist")

    def test_cli(self):
        self.assertEqual(tk.main(["fintech-trust", "--report"]), 0)
        self.assertEqual(tk.main(["nope"]), 2)


class Blueprints(unittest.TestCase):
    def test_every_page_builds_for_every_motion(self):
        for page in bp.pages():
            for motion in bp.MOTIONS:
                b = bp.build(page, motion)
                with self.subTest(page=page, motion=motion):
                    self.assertTrue(b["sections"])
                    self.assertTrue((SKILL / b["module"]).exists(), b["module"])
                    ids = [s["id"] for s in b["sections"]]
                    self.assertEqual(len(ids), len(set(ids)), ids)

    def test_motion_rules(self):
        sales = {s["id"]: s for s in bp.build("homepage", "sales-led")["sections"]}
        self.assertTrue(sales["security"]["required"])
        self.assertEqual(bp.build("homepage", "sales-led")["primary_cta"], "Get a demo")
        self.assertIn("pricing-preview", [s["id"] for s in bp.build("homepage", "self-serve")["sections"]])
        self.assertNotIn("plan-controls", [s["id"] for s in bp.build("pricing", "sales-led")["sections"]])
        self.assertNotIn("logos", [s["id"] for s in bp.build("homepage", logos=False)["sections"]])

    def test_industrial_flagged(self):
        self.assertTrue(bp.build("industrial", "service")["thin_evidence"])

    def test_homepage_order_matches_research(self):
        ids = [s["id"] for s in bp.build("homepage")["sections"]]
        self.assertLess(ids.index("hero"), ids.index("logos"))
        self.assertLess(ids.index("proof"), ids.index("cta-band"))
        self.assertEqual(ids[-1], "footer")


if __name__ == "__main__":
    unittest.main()
