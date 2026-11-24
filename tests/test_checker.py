import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "b2b-ui-designer"
sys.path.insert(0, str(SKILL / "scripts"))
import check_page as cp  # noqa: E402

HEAD = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1"><title>T</title>'
        '<meta name="description" content="d"><style>{css}</style></head><body{attrs}><main>{body}</main></body></html>')
BASE_CSS = ":root{--bg:#fff;--text:#111;--measure:65ch} body{color:var(--text);background-color:var(--bg)} p{max-width:65ch}"


def page(body="<h1>Title</h1>", css="", attrs=""):
    return HEAD.format(css=BASE_CSS + css, body=body, attrs=attrs)


def rules(res, level=None):
    items = res["errors"] + res["warnings"] if level is None else res[level]
    return {i["rule"] for i in items}


class ExamplePages(unittest.TestCase):
    def test_examples_pass_clean(self):
        examples = sorted((SKILL / "examples").glob("*.html"))
        self.assertTrue(examples)
        for ex in examples:
            html, base = cp.load(ex)
            res = cp.check(html, base)
            with self.subTest(ex.name):
                self.assertEqual(res["errors"], [])
                self.assertEqual(res["warnings"], [])
                self.assertIn("hero", res["sections"])


class SloppyFixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        html, base = cp.load(ROOT / "tests" / "fixtures" / "sloppy.html")
        cls.res = cp.check(html, base)

    def test_fails(self):
        self.assertFalse(self.res["ok"])

    def test_expected_errors(self):
        for r in ("a11y-img-alt", "a11y-label", "a11y-name", "a11y-contrast", "a11y-focus", "a11y-target",
                  "html-lang", "html-viewport", "html-main", "motion-reduced", "motion-pause", "motion-autoplay"):
            self.assertIn(r, rules(self.res, "errors"), r)

    def test_every_slop_rule_fires(self):
        for r in ("slop-gradient", "slop-gradient-text", "slop-default-color", "slop-glass", "slop-emoji",
                  "slop-buzzwords", "slop-unsourced-stat", "slop-fake-person", "slop-vague-proof", "slop-lorem",
                  "slop-generic-heading", "slop-placeholder-media"):
            self.assertIn(r, rules(self.res, "warnings"), r)

    def test_modern_web_warnings(self):
        for r in ("perf-img-dimensions", "perf-fonts", "perf-blocking-script", "css-100vh", "html-doctype",
                  "b2b-hero-buttons", "b2b-proof", "b2b-form-button", "motion-long-hover", "motion-properties"):
            self.assertIn(r, rules(self.res), r)


class Rules(unittest.TestCase):
    def test_minimal_page_is_ok(self):
        res = cp.check(page())
        self.assertTrue(res["ok"], res["errors"])

    def test_contrast_pass_and_fail(self):
        self.assertNotIn("a11y-contrast", rules(cp.check(page(css=".x{color:#595959;background-color:#fff}")), "errors"))
        self.assertIn("a11y-contrast", rules(cp.check(page(css=".x{color:#777;background-color:#fff}")), "errors"))

    def test_large_text_uses_3_to_1(self):
        css = ".x{color:#888;background-color:#fff;font-size:32px}"  # 3.54:1
        self.assertNotIn("a11y-contrast", rules(cp.check(page(css=css)), "errors"))

    def test_dark_theme_tokens_checked(self):
        css = "@media (prefers-color-scheme: dark){:root{--bg:#000;--text:#222}}"
        res = cp.check(page(css=css))
        self.assertTrue(any("dark theme" in e["message"] for e in res["errors"]), res["errors"])

    def test_wrapping_label_counts(self):
        body = '<h1>T</h1><form><label>Email <input type="email" autocomplete="email"></label></form>'
        self.assertNotIn("a11y-label", rules(cp.check(page(body=body))))

    def test_placeholder_is_not_a_label(self):
        res = cp.check(page(body='<h1>T</h1><input placeholder="Email">'))
        self.assertTrue(any("placeholder" in e["message"] for e in res["errors"]))

    def test_reduced_motion_satisfies(self):
        css = ".a{transition:opacity 200ms} @media (prefers-reduced-motion: reduce){.a{transition:none}}"
        self.assertNotIn("motion-reduced", rules(cp.check(page(css=css))))
        self.assertIn("motion-reduced", rules(cp.check(page(css=".a{transition:opacity 200ms}"))))

    def test_marquee_pause_levels(self):
        loop = ".m{animation:s 30s linear infinite}@keyframes s{to{transform:translateX(-50%)}}@media (prefers-reduced-motion: reduce){.m{animation:none}}"
        self.assertIn("motion-pause", rules(cp.check(page(css=loop)), "errors"))
        hover = loop + ".m:hover{animation-play-state:paused}"
        res = cp.check(page(css=hover))
        self.assertNotIn("motion-pause", rules(res, "errors"))
        self.assertIn("motion-pause", rules(res, "warnings"))
        focus = loop + ".m:hover,.m:focus-within{animation-play-state:paused}"
        self.assertNotIn("motion-pause", rules(cp.check(page(css=focus))))
        button = page(body='<h1>T</h1><button>Pause logos</button>', css=loop)
        self.assertNotIn("motion-pause", rules(cp.check(button)))

    def test_spinner_is_exempt(self):
        css = ".s{animation:spin 1s linear infinite}@media (prefers-reduced-motion: reduce){.s{animation:none}}"
        self.assertNotIn("motion-pause", rules(cp.check(page(css=css))))

    def test_focus_visible_replacement(self):
        self.assertIn("a11y-focus", rules(cp.check(page(css="a:focus{outline:none}"))))
        ok = "a:focus{outline:none} a:focus-visible{outline:2px solid #00f}"
        self.assertNotIn("a11y-focus", rules(cp.check(page(css=ok))))

    def test_sourced_stat_and_placeholder_ok(self):
        body = '<h1>T</h1><p data-source="Client report 2026">40% faster close</p><p>[Metric from client] 30%</p>'
        self.assertNotIn("slop-unsourced-stat", rules(cp.check(page(body=body))))
        self.assertIn("slop-unsourced-stat", rules(cp.check(page(body="<h1>T</h1><p>40% faster close</p>"))))

    def test_save_percentage_is_not_a_stat(self):
        self.assertNotIn("slop-unsourced-stat", rules(cp.check(page(body="<h1>T</h1><p>Save 20% yearly</p>"))))

    def test_primary_cta_labels(self):
        body = ('<h1>T</h1><section data-section="hero"><a data-cta="primary" href="/a">Get started</a></section>'
                '<section data-section="proof"><p>[Logo]</p></section>'
                '<section data-section="cta-band"><a data-cta="primary" href="/b">Start trial</a></section>')
        res = cp.check(page(body=body))
        self.assertTrue(any("different labels" in w["message"] for w in res["warnings"]))

    def test_proof_before_ask(self):
        body = ('<h1>T</h1><section data-section="hero"><a data-cta="primary" href="/a">Go</a></section>'
                '<section data-section="features"><a data-cta="primary" href="/a">Go</a></section>'
                '<section data-section="proof"><p>[Logo]</p></section>')
        self.assertIn("b2b-proof-before-ask", rules(cp.check(page(body=body))))

    def test_pricing_rules(self):
        res = cp.check(page(body="<h1>Pricing</h1><p>$20</p>", attrs=' data-page="pricing"'))
        self.assertIn("b2b-pricing-unit", rules(res))
        self.assertIn("b2b-pricing-enterprise", rules(res))
        ok = cp.check(page(body="<h1>Pricing</h1><p>$20 per user / month</p><p>Enterprise: contact sales</p>",
                           attrs=' data-page="pricing"'))
        self.assertNotIn("b2b-pricing-unit", rules(ok))

    def test_lazy_hero_image(self):
        body = ('<h1>T</h1><section data-section="hero"><img src="a.png" alt="" width="10" height="10" loading="lazy"></section>')
        self.assertIn("perf-lazy-hero", rules(cp.check(page(body=body))))

    def test_tailwind_slop_classes(self):
        body = '<h1 class="bg-gradient-to-r from-indigo-500 to-purple-600 bg-clip-text text-transparent">T</h1>'
        r = rules(cp.check(page(body=body)))
        self.assertTrue({"slop-gradient", "slop-gradient-text", "slop-default-color"} <= r, r)

    def test_check_marks_are_not_emoji(self):
        self.assertNotIn("slop-emoji", rules(cp.check(page(body="<h1>T</h1><ul><li>✓ SSO</li><li>★★★★★</li></ul>"))))

    def test_malformed_html_does_not_crash(self):
        res = cp.check("<div><p>unclosed <b>tags</div></span><style>.a{color:</style>")
        self.assertFalse(res["ok"])


if __name__ == "__main__":
    unittest.main()
