#!/usr/bin/env python3
"""B2B page checker (standard library only).

Usage:
  python3 check_page.py page.html [--json] [--rules]

Reads the HTML, its <style> blocks, style="" attributes and linked local stylesheets, then reports:
  a11y-*    WCAG 2.2 AA: contrast, labels, names, alt text, focus, target size
  html-*    semantic structure: lang, title, viewport, main, headings
  perf-*    Core Web Vitals hygiene: image sizing and loading, fonts, blocking scripts
  css-*     modern CSS guidance
  motion-*  reduced motion, pause controls, timing
  b2b-*     page structure and conversion: sections, primary CTA, proof, pricing, reading width
  slop-*    generic "AI slop" patterns: gradients, default colours, emoji icons, buzzwords, fake proof

Errors must be fixed. Warnings must be reviewed. Exit code 1 when there are errors.
Mark sections with data-section="hero|logos|features|proof|..." and the primary CTA with
data-cta="primary" so the structure rules can run (see references/pages/*.md).
"""
import argparse
import colorsys
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import contrast as c  # noqa: E402

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
SKIP_TEXT = {"script", "style", "template", "noscript", "svg"}
PROOF_SECTIONS = {"logos", "proof", "testimonials", "testimonial", "case-studies", "stats", "awards", "reviews", "customers"}
NON_CONTENT = {"nav", "announcement", "header", "app-shell"}
BUZZWORDS = [
    "revolutionize", "revolutionise", "revolutionary", "supercharge", "unlock", "unleash", "seamless", "seamlessly",
    "effortless", "effortlessly", "elevate", "empower", "leverage", "cutting-edge", "game-changer", "game-changing",
    "next-generation", "next-gen", "world-class", "best-in-class", "robust", "synergy", "paradigm", "disrupt",
    "fast-paced world", "next level", "transformative", "turbocharge", "skyrocket", "harness the power",
]
GENERIC_HEADINGS = {"features", "our features", "key features", "why choose us", "why us", "what we offer",
                    "our solutions", "our services", "benefits", "testimonials", "about us", "our mission",
                    "what our customers say", "what our clients say"}
DEFAULT_COLORS = {"#6366f1", "#4f46e5", "#8b5cf6", "#7c3aed", "#a855f7", "#9333ea", "#818cf8", "#c084fc"}
TW_DEFAULT = re.compile(r"\b(?:bg|text|from|to|via|border|ring)-(?:indigo|violet|purple|fuchsia)-(?:400|500|600|700)\b")
STOCK_HOSTS = ("source.unsplash.com", "images.unsplash.com", "picsum.photos", "images.pexels.com", "shutterstock.com",
               "istockphoto.com", "pravatar.cc", "randomuser.me", "ui-avatars.com", "placehold.co", "placeholder.com",
               "via.placeholder.com", "dummyimage.com", "thispersondoesnotexist.com")
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U0001F600-\U0001F64F☀-⛿✀-➿⭐⬆⤴⤵⏰-⏺]")
EMOJI_OK = set("✓✔✕✖✗✘★☆☐☑☒→←")
STAT = re.compile(r"(?<![\w$€£₹])(\d+(?:\.\d+)?x\b|\d{1,3}(?:\.\d+)?%|\d{1,3}(?:,\d{3})+\+|\d+(?:\.\d+)?[kKmMbB]\+)")
FAKE_PEOPLE = re.compile(r"\b(John|Jane) (Doe|Smith)\b|\b[A-Z][a-z]+ [A-Z]\.,? (?:CEO|CTO|COO|CFO|Founder|Co-founder|VP|Head|Director|Manager)\b")
VAGUE_PROOF = re.compile(r"trusted by (?:thousands|millions|hundreds|leading|top|the world's)|thousands of (?:companies|teams|businesses|customers)", re.I)
PRICE_UNIT = re.compile(r"per (?:user|seat|month|year|member|editor)|/\s?(?:mo|month|yr|year|user|seat)\b|billed (?:monthly|annually|yearly)", re.I)
INPUT_EXEMPT = {"hidden", "submit", "button", "reset", "image"}


# ---------------------------------------------------------------- tiny DOM

class Node:
    __slots__ = ("tag", "attrs", "children", "parent", "line")

    def __init__(self, tag, attrs, parent, line=0):
        self.tag, self.attrs, self.children, self.parent, self.line = tag, attrs, [], parent, line

    def iter(self):
        for ch in self.children:
            if isinstance(ch, Node):
                yield ch
                yield from ch.iter()

    def find_all(self, *tags):
        return [n for n in self.iter() if n.tag in tags]

    def text(self, names=False):
        """Visible text; with names=True also image alt text and aria-labels (accessible-name style)."""
        out = []
        for ch in self.children:
            if isinstance(ch, str):
                out.append(ch)
            elif ch.tag not in SKIP_TEXT and ch.attrs.get("aria-hidden") != "true" and "hidden" not in ch.attrs:
                if names and ch.tag == "img":
                    out.append(ch.attrs.get("alt") or "")
                elif names and ch.attrs.get("aria-label"):
                    out.append(ch.attrs["aria-label"])
                else:
                    out.append(ch.text(names))
        return re.sub(r"\s+", " ", " ".join(out)).strip()

    def ancestors(self):
        n = self.parent
        while n is not None:
            yield n
            n = n.parent

    def classes(self):
        return (self.attrs.get("class") or "").split()

    def describe(self):
        bits = [self.tag]
        if self.attrs.get("id"):
            bits.append("#" + self.attrs["id"])
        if self.classes():
            bits.append("." + ".".join(self.classes()[:2]))
        t = self.text(True)[:40] or self.attrs.get("placeholder", "") or self.attrs.get("name", "")
        return "".join(bits) + (f' "{t}"' if t else "") + (f" (line {self.line})" if self.line else "")


class Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#document", {}, None)
        self.stack = [self.root]
        self.doctype = False

    def handle_decl(self, decl):
        if decl.lower().startswith("doctype"):
            self.doctype = True

    def handle_starttag(self, tag, attrs):
        node = Node(tag, {k.lower(): (v if v is not None else "") for k, v in attrs}, self.stack[-1], self.getpos()[0])
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        node = Node(tag, {k.lower(): (v if v is not None else "") for k, v in attrs}, self.stack[-1], self.getpos()[0])
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        if data:
            self.stack[-1].children.append(data)


# ---------------------------------------------------------------- tiny CSS

class Rule:
    __slots__ = ("selector", "decls", "media")

    def __init__(self, selector, decls, media):
        self.selector, self.decls, self.media = selector, decls, media

    @property
    def theme(self):
        s, m = self.selector.replace("'", '"').replace(" ", ""), self.media.replace(" ", "").lower()
        if 'data-theme="dark"' in s or "data-theme=dark" in s or s.startswith(".dark"):
            return "dark"
        if 'data-theme="light"' in s or "data-theme=light" in s:
            return "light"
        if "prefers-color-scheme:dark" in m:
            return "dark"
        if "prefers-color-scheme:light" in m:
            return "light"
        return None


def _decls(body):
    out, depth, buf = {}, 0, ""
    for ch in body:  # ignore nested blocks (CSS nesting)
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        elif depth == 0:
            buf += ch
    for part in buf.split(";"):
        if ":" in part:
            k, v = part.split(":", 1)
            k = k.strip().lower()
            if k:
                out[k] = re.sub(r"\s*!important\s*$", "", v.strip())
    return out


def _block_end(text, start):
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    return len(text) - 1


def parse_css(text, media=""):
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    rules, keyframes, fontfaces = [], [], []
    i = 0
    while True:
        j = text.find("{", i)
        if j < 0:
            break
        prelude = text[i:j].split(";")[-1].strip()
        end = _block_end(text, j)
        body = text[j + 1:end]
        low = prelude.lower()
        if low.startswith("@media"):
            r, k, f = parse_css(body, (media + " and " if media else "") + prelude[6:].strip())
            rules += r; keyframes += k; fontfaces += f  # noqa: E702
        elif low.startswith(("@supports", "@layer", "@container", "@scope", "@starting-style")):
            r, k, f = parse_css(body, media)
            rules += r; keyframes += k; fontfaces += f  # noqa: E702
        elif "keyframes" in low:
            keyframes.append(prelude.split()[-1] if prelude.split() else "")
        elif low.startswith("@font-face"):
            fontfaces.append(_decls(body))
        elif prelude and not low.startswith("@"):
            d = _decls(body)
            for sel in prelude.split(","):
                rules.append(Rule(sel.strip(), d, media))
        i = end + 1
    return rules, keyframes, fontfaces


def _ms(v):
    v = v.strip().lower()
    try:
        if v.endswith("ms"):
            return float(v[:-2])
        if v.endswith("s"):
            return float(v[:-1]) * 1000
    except ValueError:
        pass
    return None


def _durations(value):
    """Durations in a transition / animation value (first time token of each comma part)."""
    out = []
    for part in value.split(","):
        times = [_ms(t) for t in part.split() if _ms(t) is not None]
        if times:
            out.append(times[0])
    return out


def _px(v):
    v = (v or "").strip().lower()
    m = re.match(r"clamp\(([^,]+),", v) or re.match(r"min\(([^,]+),", v)
    if m:
        v = m.group(1).strip()
    m = re.fullmatch(r"(-?[\d.]+)(px|rem|em)?", v)
    if not m:
        return None
    n = float(m.group(1))
    return n * 16 if m.group(2) in ("rem", "em") else n


# ---------------------------------------------------------------- checker

class Report:
    def __init__(self):
        self.errors, self.warnings, self._seen = [], [], set()

    def add(self, level, rule, message, where=""):
        key = (rule, message, where)
        if key in self._seen:
            return
        self._seen.add(key)
        (self.errors if level == "error" else self.warnings).append({"rule": rule, "message": message, "where": where})


def load(path):
    path = Path(path)
    return path.read_text(encoding="utf-8", errors="replace"), path.parent


def check(html, base_dir=None):
    b = Builder()
    b.feed(html)
    doc = b.root
    rep = Report()

    # ---- gather CSS
    css_parts = ["".join(ch for ch in n.children if isinstance(ch, str)) for n in doc.find_all("style")]
    links = [n for n in doc.find_all("link") if "stylesheet" in (n.attrs.get("rel") or "").lower()]
    for ln in links:
        href = ln.attrs.get("href", "")
        if base_dir and href and not re.match(r"^[a-z]+:|^//", href):
            p = (Path(base_dir) / href.split("?")[0]).resolve()
            if p.is_file():
                css_parts.append(p.read_text(encoding="utf-8", errors="replace"))
    inline = [n for n in doc.iter() if n.attrs.get("style")]
    css_text = "\n".join(css_parts)
    rules, keyframes, fontfaces = parse_css(css_text)
    for n in inline:
        rules.append(Rule(f"[style] {n.tag}", _decls(n.attrs["style"]), ""))
    all_decl_text = css_text + "\n" + "\n".join(n.attrs["style"] for n in inline)

    # ---- variables per theme
    def rootish(sel):
        return sel.startswith(":root") or sel in ("html", "body") or sel.startswith("html[")
    base = {}
    for r in rules:
        if r.theme is None and rootish(r.selector) and "print" not in r.media:
            base.update({k: v for k, v in r.decls.items() if k.startswith("--")})
    themes = {"default": base}
    for r in rules:
        if r.theme and rootish(r.selector):
            themes.setdefault(r.theme, dict(base)).update({k: v for k, v in r.decls.items() if k.startswith("--")})

    def resolve(v, vars_, depth=0):
        if v is None or depth > 10 or "var(" not in v:
            return v
        def sub(m):
            inner = m.group(1)
            name, _, fb = inner.partition(",")
            val = vars_.get(name.strip())
            return resolve(val, vars_, depth + 1) if val is not None else (fb.strip() or "")
        return resolve(re.sub(r"var\(([^()]*(?:\([^()]*\)[^()]*)*)\)", sub, v), vars_, depth + 1)

    def color_of(v):
        if not v or "gradient(" in v or "url(" in v:
            return None
        try:
            return c.parse(v.strip())
        except c.ColorError:
            for tok in re.findall(r"#[0-9a-fA-F]{3,8}\b|(?:rgb|hsl)a?\([^)]*\)|\bwhite\b|\bblack\b", v):
                try:
                    return c.parse(tok)
                except c.ColorError:
                    pass
        return None

    # ================================================================ html-*
    html_el = next((n for n in doc.iter() if n.tag == "html"), None)
    if not b.doctype:
        rep.add("warning", "html-doctype", "Missing <!doctype html>; the page renders in quirks mode.")
    if html_el is None or not html_el.attrs.get("lang"):
        rep.add("error", "html-lang", "Set the page language: <html lang=\"en\">. [WCAG 3.1.1]")
    titles = doc.find_all("title")
    if not titles or not titles[0].text():
        rep.add("error", "html-title", "Add a descriptive <title>. [WCAG 2.4.2]")
    metas = doc.find_all("meta")
    if not any(m.attrs.get("name", "").lower() == "viewport" for m in metas):
        rep.add("error", "html-viewport", 'Add <meta name="viewport" content="width=device-width, initial-scale=1">.')
    if not any(m.attrs.get("charset") for m in metas):
        rep.add("warning", "html-charset", 'Add <meta charset="utf-8"> as the first element in <head>.')
    if not any(m.attrs.get("name", "").lower() == "description" and m.attrs.get("content") for m in metas):
        rep.add("warning", "html-description", "Add a <meta name=\"description\"> for search results and link previews.")
    mains = doc.find_all("main")
    if len(mains) != 1:
        rep.add("error", "html-main", f"Use exactly one <main> landmark (found {len(mains)}). [WCAG 1.3.1]")
    h1s = doc.find_all("h1")
    if not h1s:
        rep.add("error", "html-h1", "Add one <h1> stating what the page is about. [WCAG 1.3.1]")
    elif len(h1s) > 1:
        rep.add("warning", "html-h1", f"{len(h1s)} <h1> elements; use one and h2 for sections.")
    last = 0
    for h in doc.find_all("h1", "h2", "h3", "h4", "h5", "h6"):
        lvl = int(h.tag[1])
        if last and lvl > last + 1:
            rep.add("warning", "html-heading-order", f"Heading jumps from h{last} to h{lvl}.", h.describe())
        last = lvl
    for n in doc.iter():
        if n.tag in ("div", "span") and "onclick" in n.attrs and n.attrs.get("role") not in ("button", "link"):
            rep.add("warning", "html-clickable-div", "Clickable <div>/<span>; use <button> or <a href>. [WCAG 4.1.2]", n.describe())

    # ================================================================ a11y-*
    for img in doc.find_all("img"):
        if "alt" not in img.attrs:
            rep.add("error", "a11y-img-alt", 'Image without alt; describe it, or alt="" if decorative. [WCAG 1.1.1]', img.describe())
    label_for = {lb.attrs.get("for") for lb in doc.find_all("label") if lb.attrs.get("for")}
    for f in doc.find_all("input", "select", "textarea"):
        if f.tag == "input" and f.attrs.get("type", "text").lower() in INPUT_EXEMPT:
            continue
        named = (f.attrs.get("id") in label_for or any(a.tag == "label" for a in f.ancestors())
                 or f.attrs.get("aria-label") or f.attrs.get("aria-labelledby") or f.attrs.get("title"))
        if not named:
            msg = "Form field has no label"
            if f.attrs.get("placeholder"):
                msg += " (a placeholder is not a label)"
            rep.add("error", "a11y-label", msg + ". [WCAG 3.3.2, 1.3.1]", f.describe())
    for btn in doc.find_all("button"):
        if not (btn.text(True) or btn.attrs.get("aria-label") or btn.attrs.get("aria-labelledby") or btn.attrs.get("title")):
            rep.add("error", "a11y-name", "Button has no accessible name; add text or aria-label. [WCAG 4.1.2]", btn.describe())
    for a in doc.find_all("a"):
        if "href" in a.attrs and not (a.text(True) or a.attrs.get("aria-label") or a.attrs.get("aria-labelledby") or a.attrs.get("title")):
            rep.add("error", "a11y-name", "Link has no accessible name. [WCAG 2.4.4]", a.describe())

    # contrast: rules that set both color and background
    def is_large(decls, vars_):
        size = _px(resolve(decls.get("font-size"), vars_))
        weight = resolve(decls.get("font-weight"), vars_) or ""
        bold = weight.strip() in ("bold", "bolder") or (weight.strip().isdigit() and int(weight) >= 700)
        return size is not None and (size >= 24 or (size >= 18.66 and bold))

    checked_pairs = 0
    for r in rules:
        if "print" in r.media or "color" not in r.decls:
            continue
        bgv = r.decls.get("background-color") or r.decls.get("background")
        if not bgv:
            continue
        for tname, vars_ in themes.items():
            if r.theme and r.theme != tname:
                continue
            fg, bg = color_of(resolve(r.decls["color"], vars_)), color_of(resolve(bgv, vars_))
            # A fully transparent background shows whatever is behind it, which one rule can't tell us.
            if not fg or not bg or bg[3] == 0:
                continue
            checked_pairs += 1
            ratio = c.ratio(fg, bg)
            need = 3.0 if is_large(r.decls, vars_) else 4.5
            if ratio < need:
                rep.add("error", "a11y-contrast", f"Text contrast {ratio:.2f}:1 is below {need}:1 ({tname} theme). [WCAG 1.4.3]",
                        r.selector)
    # contrast: this skill's token pairs, when the page uses them
    for tname, vars_ in themes.items():
        for fgk, bgk, need in (("--text", "--bg", 4.5), ("--text-muted", "--bg", 4.5), ("--text-muted", "--bg-subtle", 4.5),
                               ("--text", "--surface", 4.5), ("--accent-contrast", "--accent", 4.5),
                               ("--accent-text", "--bg", 4.5), ("--focus", "--bg", 3.0)):
            if fgk in vars_ and bgk in vars_:
                fg, bg = color_of(resolve(vars_[fgk], vars_)), color_of(resolve(vars_[bgk], vars_))
                if fg and bg:
                    checked_pairs += 1
                    ratio = c.ratio(fg, bg)
                    if ratio < need:
                        rep.add("error", "a11y-contrast", f"{fgk} on {bgk} is {ratio:.2f}:1, below {need}:1 ({tname} theme). [WCAG 1.4.3/1.4.11]", ":root")
    if checked_pairs == 0:
        rep.add("warning", "a11y-contrast", "Couldn't find text/background pairs to measure; check contrast with contrast.py or tokens.py --report.")

    # focus visibility
    kills_outline = [r for r in rules if re.fullmatch(r"(none|0|0px)", (r.decls.get("outline") or "x").strip())]
    has_focus_visible = any(":focus-visible" in r.selector and ("outline" in r.decls or "box-shadow" in r.decls) for r in rules)
    if kills_outline and not has_focus_visible:
        rep.add("error", "a11y-focus", "Focus outline removed with no :focus-visible replacement. [WCAG 2.4.7]", kills_outline[0].selector)

    # target size
    for r in rules:
        sel = r.selector.lower()
        if re.search(r"(^|[\s>+~])button|\.btn|button\b|\[type=.?submit|\.button|\.cta", sel):
            for prop in ("min-height", "height"):
                v = _px(resolve(r.decls.get(prop), themes["default"]))
                if v is not None and 0 < v < 24:
                    rep.add("error", "a11y-target", f"Button {prop} {v:g}px is under the 24px minimum. [WCAG 2.5.8]", r.selector)
                elif v is not None and 24 <= v < 44 and "primary" in sel:
                    rep.add("warning", "a11y-target", f"Primary button {prop} {v:g}px; 44px is recommended on touch. [WCAG 2.5.5]", r.selector)

    # ================================================================ motion-*
    trans_rules = [r for r in rules if any(d > 0 for d in _durations(r.decls.get("transition", "") + "," + r.decls.get("transition-duration", "")))]
    anim_rules = [r for r in rules if (r.decls.get("animation") or r.decls.get("animation-name", "none")).strip() not in ("", "none")]
    has_reduced = "prefers-reduced-motion" in all_decl_text
    if (trans_rules or anim_rules or keyframes) and not has_reduced:
        rep.add("error", "motion-reduced", "Page has motion but no prefers-reduced-motion handling. [WCAG 2.3.3]")
    essential = re.compile(r"spin|load|shimmer|skeleton|pulse|progress", re.I)
    infinite = [r for r in anim_rules if "infinite" in (r.decls.get("animation", "") + r.decls.get("animation-iteration-count", ""))
                and not essential.search(r.decls.get("animation", "") + r.decls.get("animation-name", ""))
                and "reduce" not in r.media]
    pause_button = any(re.search(r"\bpause\b", (n.text(True) + " " + n.attrs.get("aria-label", "")).lower())
                       for n in doc.find_all("button"))
    pause_css = [r for r in rules if (r.decls.get("animation-play-state") or "").strip() == "paused"]
    if infinite and not pause_button:
        if any(":focus-within" in r.selector for r in pause_css):
            pass
        elif pause_css:
            rep.add("warning", "motion-pause", "Looping animation pauses on hover only; add a pause button or pause on :focus-within. [WCAG 2.2.2]", infinite[0].selector)
        else:
            rep.add("error", "motion-pause", "Looping animation with no way to pause it. [WCAG 2.2.2]", infinite[0].selector)
    for v in doc.find_all("video"):
        if "autoplay" in v.attrs:
            if "muted" not in v.attrs:
                rep.add("error", "motion-autoplay", "Autoplaying video must be muted.", v.describe())
            if "controls" not in v.attrs and not pause_button:
                rep.add("error", "motion-pause", "Autoplaying video needs controls or a pause button. [WCAG 2.2.2]", v.describe())
            if "playsinline" not in v.attrs:
                rep.add("warning", "perf-video", "Add playsinline so iOS doesn't open the video full screen.", v.describe())
    for r in trans_rules:
        ds = _durations(r.decls.get("transition", "") + "," + r.decls.get("transition-duration", ""))
        sel = r.selector.lower()
        if max(ds) > 300 and re.search(r"button|\.btn|(^|[\s>])a([\s:.\[]|$)|link|:hover", sel):
            rep.add("warning", "motion-long-hover", f"{max(ds):g}ms transition on an interactive element; keep feedback ≤ 300ms.", r.selector)
        elif max(ds) > 1000:
            rep.add("warning", "motion-long", f"{max(ds):g}ms transition; B2B motion rarely needs more than 800ms.", r.selector)
    for r in rules:
        tv = r.decls.get("transition", "")
        if re.search(r"\b(width|height|top|left|margin|padding)\b", tv) or tv.strip().startswith("all"):
            rep.add("warning", "motion-properties", "Transition animates layout (or 'all'); animate transform and opacity only.", r.selector)

    # ================================================================ perf-* and css-*
    imgs = doc.find_all("img")
    sections = _sections(doc)
    first_content = next((s for s in sections if s[0] not in NON_CONTENT), None)
    hero_node = next((n for sid, n in sections if sid == "hero"), first_content[1] if first_content else None)
    hero_imgs = set(id(i) for i in hero_node.find_all("img")) if hero_node is not None else set()
    missing_dims = [i for i in imgs if not (i.attrs.get("width") and i.attrs.get("height")) and "aspect-ratio" not in (i.attrs.get("style") or "")]
    if missing_dims:
        rep.add("warning", "perf-img-dimensions", f"{len(missing_dims)} image(s) without width and height; this causes layout shift (CLS).", missing_dims[0].describe())
    for i in imgs:
        if id(i) in hero_imgs and i.attrs.get("loading") == "lazy":
            rep.add("warning", "perf-lazy-hero", "Hero image is lazy-loaded; this delays LCP. Use fetchpriority=\"high\" instead.", i.describe())
    eager_below = [i for i in imgs if id(i) not in hero_imgs and i.attrs.get("loading") != "lazy"
                   and not any(a.tag in ("header", "nav") for a in i.ancestors())]
    if hero_node is not None and eager_below:
        rep.add("warning", "perf-lazy-below", f"{len(eager_below)} below-the-fold image(s) without loading=\"lazy\".", eager_below[0].describe())
    families = set()
    for ln in links:
        href = ln.attrs.get("href", "")
        if "fonts.googleapis.com" in href:
            families |= {f.split(":")[0].replace("+", " ") for f in re.findall(r"family=([^&]+)", href)}
            if "display=swap" not in href:
                rep.add("warning", "perf-fonts", "Google Fonts link without &display=swap; text stays invisible while fonts load.", href[:80])
    for ff in fontfaces:
        if ff.get("font-family"):
            families.add(ff["font-family"].strip("\"' "))
        if "font-display" not in ff:
            rep.add("warning", "perf-fonts", "@font-face without font-display: swap.", ff.get("font-family", ""))
    non_mono = {f for f in families if "mono" not in f.lower() and "code" not in f.lower()}
    if len(non_mono) > 2:
        rep.add("warning", "perf-fonts", f"{len(non_mono)} font families ({', '.join(sorted(non_mono))}); use at most 2 plus a mono.")
    head = next((n for n in doc.iter() if n.tag == "head"), None)
    if head is not None:
        for s in head.find_all("script"):
            if s.attrs.get("src") and not ({"defer", "async"} & set(s.attrs)) and s.attrs.get("type") != "module":
                rep.add("warning", "perf-blocking-script", "Render-blocking script in <head>; add defer.", s.attrs.get("src", "")[:80])
    if re.search(r"(?<![\w.])100vh\b", all_decl_text):
        rep.add("warning", "css-100vh", "100vh jumps with mobile browser bars; use 100dvh or 100svh.")
    if len(themes) > 1 and "color-scheme" not in all_decl_text and not any(m.attrs.get("name") == "color-scheme" for m in metas):
        rep.add("warning", "css-no-dark-scheme", "Dark theme defined without color-scheme; form controls and scrollbars stay light.")

    # ================================================================ b2b-*
    page_type = (doc.find_all("body") or [Node("body", {}, None)])[0].attrs.get("data-page", "")
    marked = [n for n in doc.iter() if n.attrs.get("data-section")]
    ids = [sid for sid, _ in sections]
    if not marked:
        rep.add("warning", "b2b-sections", "No data-section attributes; structure rules guessed from <section> ids and classes.")
    is_app = page_type.startswith("app") or "app-shell" in ids
    primaries = [n for n in doc.iter() if n.attrs.get("data-cta") == "primary"]
    if not is_app and page_type not in ("demo-request",):
        if not primaries:
            rep.add("warning", "b2b-primary-cta", 'Mark the primary CTA with data-cta="primary" (one conversion per page).')
        else:
            labels = {re.sub(r"\s+", " ", p.text(True)).strip().lower() for p in primaries}
            if len(labels) > 1:
                rep.add("warning", "b2b-primary-cta", f"Primary CTA uses {len(labels)} different labels ({', '.join(sorted(labels))}); use one label everywhere.")
            # Pricing pages put the conversion in the plan cards right below a short hero (pages/pricing.md).
            first_ask = next((n for sid, n in sections if sid == "plans"), hero_node) if page_type == "pricing" else hero_node
            if first_ask is not None and not any(p is first_ask or first_ask in list(p.ancestors()) for p in primaries):
                place = "The hero has" if first_ask is hero_node else "The plan cards have"
                rep.add("warning", "b2b-primary-cta", f"{place} no primary CTA.")
            content = [s for s in ids if s not in NON_CONTENT]
            if len(content) >= 6 and len(primaries) < 3:
                rep.add("warning", "b2b-primary-cta", f"Long page ({len(content)} sections) shows the primary CTA {len(primaries)} time(s); repeat it every 2-3 sections and in a final cta-band.")
        if hero_node is not None:
            buttons = [n for n in hero_node.iter() if n.tag == "button" or n.attrs.get("data-cta")
                       or (n.tag == "a" and any("btn" in cl or "button" in cl for cl in n.classes()))]
            if len(buttons) > 2:
                rep.add("warning", "b2b-hero-buttons", f"Hero has {len(buttons)} buttons; keep 2 at most and make the rest text links.")
        if page_type in ("", "homepage", "product-feature", "solution", "industrial"):
            if not PROOF_SECTIONS & set(ids):
                rep.add("warning", "b2b-proof", "No proof section (logos, proof, testimonials, case-studies, stats); B2B buyers look for named evidence.")
            else:
                idx = {sid: i for i, sid in reversed(list(enumerate(ids)))}
                first_proof = min(idx[s] for s in PROOF_SECTIONS & set(ids))
                hero_i = ids.index("hero") if "hero" in ids else 0
                for i, (sid, node) in enumerate(sections):
                    if i > hero_i and sid not in NON_CONTENT and any(p is node or node in list(p.ancestors()) for p in primaries):
                        if i < first_proof:
                            rep.add("warning", "b2b-proof-before-ask", f"A primary CTA in '{sid}' comes before any proof; show logos or results first.")
                        break
        if ids.count("cta-band") > 1:
            rep.add("warning", "b2b-cta-band", "More than one full-width CTA band; keep one loud ask per page.")
    if page_type == "pricing" or any("pricing" == h.text().strip().lower() for h in h1s):
        body_text = doc.text()
        if not PRICE_UNIT.search(body_text):
            rep.add("warning", "b2b-pricing-unit", "No price unit found (per user / month, billed annually); every price needs one.")
        if not re.search(r"contact sales|talk to sales|enterprise|custom", body_text, re.I):
            rep.add("warning", "b2b-pricing-enterprise", "No enterprise or contact-sales path on the pricing page.")
    measure_rules = [r for r in rules if "max-width" in r.decls and (re.search(r"(^|[\s>])p\b|prose|lead|text|copy|measure|body", r.selector) or "--measure" in r.decls.get("max-width", ""))]
    if not measure_rules and "--measure" not in base:
        rep.add("warning", "b2b-measure", "No reading width set for body text; cap paragraphs around 65ch.")
    for r in measure_rules:
        m = re.match(r"([\d.]+)ch", resolve(r.decls["max-width"], themes["default"]) or "")
        if m and float(m.group(1)) > 80:
            rep.add("warning", "b2b-measure", f"Text width {m.group(1)}ch; keep lines at 60-75 characters.", r.selector)
    for form in doc.find_all("form"):
        fields = [f for f in form.find_all("input", "select", "textarea") if f.attrs.get("type", "text") not in INPUT_EXEMPT]
        if any("required" in f.attrs for f in fields) and len(fields) > 1 and not re.search(r"optional|required|\*", form.text(), re.I):
            rep.add("warning", "b2b-form-required", "Form has required fields but doesn't mark required or optional ones. [BAY]", form.describe())
        for f in fields:
            t = f.attrs.get("type", "text")
            if (t == "email" or f.attrs.get("name", "") in ("name", "email", "company", "organization", "phone")) and "autocomplete" not in f.attrs:
                rep.add("warning", "b2b-form-autocomplete", "Add autocomplete to personal fields. [WCAG 1.3.5]", f.describe())
        for s in form.find_all("button", "input"):
            label = (s.text(True) if s.tag == "button" else s.attrs.get("value", "")).strip().lower()
            if label == "submit" and (s.tag == "button" or s.attrs.get("type") == "submit"):
                rep.add("warning", "b2b-form-button", 'Submit button says "Submit"; name the action ("Book my demo").', s.describe())

    # ================================================================ slop-*
    classes_all = " ".join(" ".join(n.classes()) for n in doc.iter())
    gradients = re.findall(r"(?:linear|radial|conic)-gradient\(([^;]*)\)", all_decl_text)
    for g in gradients:
        hues = []
        for tok in re.findall(r"#[0-9a-fA-F]{3,8}\b|(?:rgb|hsl)a?\([^)]*\)", resolve(g, themes["default"]) or g):
            try:
                rgb = c.parse(tok)
            except c.ColorError:
                continue
            h, l, s = colorsys.rgb_to_hls(*(v / 255 for v in rgb[:3]))
            if s > 0.35 and 0.2 < l < 0.85:
                hues.append(h * 360)
        if len(hues) >= 2 and any(225 <= h <= 335 for h in hues) and max(hues) - min(hues) > 25:
            rep.add("warning", "slop-gradient", "Purple/indigo multi-hue gradient: the generic AI-startup look. Use a brand accent on a neutral ground.", g[:60])
            break
    if re.search(r"bg-gradient-to-\w+", classes_all) and re.search(r"\bfrom-(?:indigo|purple|violet|fuchsia|pink|blue)-\d+", classes_all):
        rep.add("warning", "slop-gradient", "Tailwind indigo/purple gradient classes: the generic AI-startup look.")
    if re.search(r"background-clip\s*:\s*text", all_decl_text) or ("bg-clip-text" in classes_all and "text-transparent" in classes_all):
        rep.add("warning", "slop-gradient-text", "Gradient-filled text; use solid text and at most one accent-coloured phrase.")
    used_defaults = sorted({h.lower() for h in re.findall(r"#[0-9a-fA-F]{6}\b", all_decl_text)} & DEFAULT_COLORS)
    if used_defaults or TW_DEFAULT.search(classes_all):
        rep.add("warning", "slop-default-color", "Default framework indigo/violet colours" + (f" ({', '.join(used_defaults)})" if used_defaults else "") + "; choose a deliberate accent with tokens.py.")
    glass = len(re.findall(r"backdrop-filter\s*:\s*[^;]*blur", all_decl_text)) + len(re.findall(r"\bbackdrop-blur", classes_all))
    if glass > 2:
        rep.add("warning", "slop-glass", f"{glass} blurred glass surfaces; keep at most one (e.g. a sticky nav).")
    emoji_hits = []
    for n in doc.find_all("h1", "h2", "h3", "h4", "button", "a", "li", "dt", "summary"):
        own = "".join(ch for ch in n.children if isinstance(ch, str))
        found = [e for e in EMOJI.findall(own) if e not in EMOJI_OK]
        if found:
            emoji_hits.append(f"{n.tag}: {''.join(found)}")
    if emoji_hits:
        rep.add("warning", "slop-emoji", f"Emoji used as icons ({'; '.join(emoji_hits[:4])}); use a consistent icon set or none.")
    visible = doc.text()
    low = visible.lower()
    buzz = sorted({w for w in BUZZWORDS if re.search(r"\b" + re.escape(w) + r"\b", low)})
    if len(buzz) >= 3:
        rep.add("warning", "slop-buzzwords", f"Buzzwords: {', '.join(buzz)}. Say what the product does, for whom, with a specific result.")
    elif buzz:
        rep.add("warning", "slop-buzzwords", f"Buzzword(s): {', '.join(buzz)}. Replace with a concrete claim.")
    unsourced = []
    # App screens show the user's own data (KPIs, tables); only marketing claims need a source.
    for n in ([] if is_app else doc.iter()):
        if n.tag in SKIP_TEXT:
            continue
        own = "".join(ch for ch in n.children if isinstance(ch, str))
        for m in STAT.finditer(own):
            ctx = own[max(0, m.start() - 12):m.end() + 12].lower()
            if re.search(r"save|off|discount|\[|uptime sla", ctx):
                continue
            scope = [n] + list(n.ancestors())[:4]
            if any(a.attrs.get("data-source") or a.find_all("cite") for a in scope) or \
               any(re.search(r"source|as of|according to|\[metric", a.text().lower()) for a in scope[:3]):
                continue
            unsourced.append(m.group(0))
    if unsourced:
        rep.add("warning", "slop-unsourced-stat", f"Stats without a source: {', '.join(dict.fromkeys(unsourced))}. Add data-source, a <cite>, or a [Metric from client] placeholder.")
    people = sorted(set(m.group(0) for m in FAKE_PEOPLE.finditer(visible)))
    if people:
        rep.add("warning", "slop-fake-person", f"Placeholder-style people: {', '.join(people[:4])}. Use real named quotes or a labelled placeholder.")
    if VAGUE_PROOF.search(visible):
        rep.add("warning", "slop-vague-proof", f"Vague proof (\"{VAGUE_PROOF.search(visible).group(0)}\"); name customers or remove it.")
    if re.search(r"lorem ipsum|your headline here|dolor sit amet", low):
        rep.add("warning", "slop-lorem", "Lorem ipsum or template filler text left in the page.")
    for h in doc.find_all("h2", "h3"):
        t = re.sub(r"[^\w\s]", "", h.text().lower()).strip()
        if t in GENERIC_HEADINGS:
            rep.add("warning", "slop-generic-heading", f'Generic section title "{h.text()}"; state the benefit instead.', h.describe())
    for n in doc.iter():
        src = n.attrs.get("src", "") + " " + n.attrs.get("poster", "")
        if any(host in src for host in STOCK_HOSTS):
            rep.add("warning", "slop-placeholder-media", "Stock or placeholder media host; use real product UI, customers or facilities.", n.describe())

    return {"ok": not rep.errors, "errors": rep.errors, "warnings": rep.warnings,
            "sections": ids, "summary": _summary(rep)}


def _sections(doc):
    """(id, node) for each page section in document order."""
    out = []
    for n in doc.iter():
        sid = n.attrs.get("data-section")
        if sid:
            if not any(a.attrs.get("data-section") for a in n.ancestors()):
                out.append((sid.strip().lower(), n))
        elif n.tag in ("section", "nav", "footer") and not any(a.attrs.get("data-section") or a.tag == "section" for a in n.ancestors()):
            guess = (n.attrs.get("id") or (n.classes()[0] if n.classes() else n.tag)).lower()
            out.append((n.tag if n.tag in ("nav", "footer") else guess, n))
    return out


def _summary(rep):
    out = {}
    for level, items in (("errors", rep.errors), ("warnings", rep.warnings)):
        for it in items:
            cat = it["rule"].split("-")[0]
            out.setdefault(cat, {"errors": 0, "warnings": 0})[level] += 1
    return out


CATEGORY = {"a11y": "Accessibility", "html": "Semantic HTML", "perf": "Performance", "css": "Modern CSS",
            "motion": "Motion", "b2b": "B2B structure and conversion", "slop": "AI slop"}


def to_text(res):
    lines = []
    if res["sections"]:
        lines.append("Sections: " + " → ".join(res["sections"]))
    for level in ("errors", "warnings"):
        items = res[level]
        if not items:
            continue
        lines.append(f"\n{level.upper()} ({len(items)})")
        for cat in CATEGORY:
            group = [i for i in items if i["rule"].split("-")[0] == cat]
            if group:
                lines.append(f"  {CATEGORY[cat]}")
                for i in group:
                    lines.append(f"    [{i['rule']}] {i['message']}" + (f"  — {i['where']}" if i["where"] else ""))
    lines.append(f"\n{'OK' if res['ok'] else 'NOT OK'}: {len(res['errors'])} error(s), {len(res['warnings'])} warning(s)")
    return "\n".join(lines) + "\n"


def main(argv=None):
    p = argparse.ArgumentParser(description="Check a B2B page for accessibility, modern-web, motion, conversion and AI-slop issues.")
    p.add_argument("html", nargs="?")
    p.add_argument("--json", action="store_true")
    p.add_argument("--rules", action="store_true", help="list the rule families")
    a = p.parse_args(argv)
    if a.rules or not a.html:
        print(__doc__.split("Errors must")[0].split("then reports:")[1].rstrip())
        return 0
    try:
        html, base = load(a.html)
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    res = check(html, base)
    print(json.dumps(res, indent=2, ensure_ascii=False) if a.json else to_text(res), end="")
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
