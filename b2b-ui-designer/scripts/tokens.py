#!/usr/bin/env python3
"""Design tokens for a B2B style direction (standard library only).

Usage:
  python3 tokens.py <direction> [--accent #hex] [--format css|json|tailwind] [--report]
  python3 tokens.py --list

Directions: enterprise, modern-saas, fintech-trust, developer, editorial (see references/styles.md).

The accent keeps its hue but its lightness is adjusted so that:
  * text on an accent-filled button reaches 4.5:1 (--accent / --accent-contrast),
  * accent-coloured links on the page background reach 4.5:1 (--accent-text),
  * the focus ring reaches 3:1 (--focus).
--report prints every text/background pair with its contrast ratio.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import contrast as c  # noqa: E402

LIGHT_NEUTRALS = {
    "cool": {"bg": "#ffffff", "bg-subtle": "#f5f7fa", "surface": "#ffffff", "border": "#e3e8ef",
             "border-strong": "#c5cdd8", "text": "#0f172a", "text-muted": "#4b5565"},
    "warm": {"bg": "#faf9f6", "bg-subtle": "#f2f0ea", "surface": "#ffffff", "border": "#e6e2d8",
             "border-strong": "#cfc8b8", "text": "#1a1814", "text-muted": "#55504a"},
    "paper": {"bg": "#fbfaf7", "bg-subtle": "#f3f1ec", "surface": "#fbfaf7", "border": "#dedad1",
              "border-strong": "#bdb6a8", "text": "#16140f", "text-muted": "#57524a"},
}
DARK_NEUTRALS = {
    "cool": {"bg": "#0b0f17", "bg-subtle": "#111723", "surface": "#141b28", "border": "#243044",
             "border-strong": "#3a4a63", "text": "#e8edf5", "text-muted": "#a3adbd"},
    "ink": {"bg": "#0a0a0b", "bg-subtle": "#0f0f12", "surface": "#141418", "border": "#26262c",
            "border-strong": "#3b3b44", "text": "#ededef", "text-muted": "#a1a1aa"},
    "warm": {"bg": "#12110f", "bg-subtle": "#181714", "surface": "#1e1c19", "border": "#2f2c27",
             "border-strong": "#47423a", "text": "#f1eee8", "text-muted": "#b0aa9f"},
}
STATUS = {
    "light": {"success": "#0f7a3d", "warning": "#9a5b00", "danger": "#c4251c", "info": "#1f5fbf"},
    "dark": {"success": "#4ade80", "warning": "#fbbf24", "danger": "#f87171", "info": "#60a5fa"},
}
SANS_FALLBACK = 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif'
MONO_FALLBACK = 'ui-monospace, "SF Mono", Menlo, Consolas, monospace'
SERIF_FALLBACK = 'Georgia, "Times New Roman", serif'

DIRECTIONS = {
    "enterprise": {
        "summary": "Calm, dense, trustworthy. Borders over shadows, real photography, minimal motion.",
        "default_mode": "light", "light": "cool", "dark": "cool", "accent": "#0b5cad",
        "fonts": {"display": ("Inter", SANS_FALLBACK), "body": ("Inter", SANS_FALLBACK), "mono": ("IBM Plex Mono", MONO_FALLBACK)},
        "display_weight": 650, "radius": (4, 6, 8), "elevation": "border", "section_pad": 80, "density": "high",
    },
    "modern-saas": {
        "summary": "Clean and light, one saturated accent, product UI everywhere, soft shadows.",
        "default_mode": "light", "light": "cool", "dark": "cool", "accent": "#2563eb",
        "fonts": {"display": ("Inter", SANS_FALLBACK), "body": ("Inter", SANS_FALLBACK), "mono": ("JetBrains Mono", MONO_FALLBACK)},
        "display_weight": 650, "radius": (8, 12, 16), "elevation": "shadow", "section_pad": 112, "density": "medium",
    },
    "fintech-trust": {
        "summary": "Warm off-white, heavy headline, one strong accent, real numbers up front.",
        "default_mode": "light", "light": "warm", "dark": "warm", "accent": "#e8590c",
        "fonts": {"display": ("Inter", SANS_FALLBACK), "body": ("Inter", SANS_FALLBACK), "mono": ("JetBrains Mono", MONO_FALLBACK)},
        "display_weight": 750, "radius": (6, 10, 14), "elevation": "shadow-light", "section_pad": 112, "density": "medium",
    },
    "developer": {
        "summary": "Dark by default, mono accents, thin borders, code and diagrams, subtle glow.",
        "default_mode": "dark", "light": "cool", "dark": "ink", "accent": "#a3e635",
        "fonts": {"display": ("Geist", SANS_FALLBACK), "body": ("Geist", SANS_FALLBACK), "mono": ("Geist Mono", MONO_FALLBACK)},
        "display_weight": 600, "radius": (6, 8, 12), "elevation": "glow", "section_pad": 96, "density": "medium-high",
    },
    "editorial": {
        "summary": "Serif display, generous whitespace, rules instead of cards, case-study led.",
        "default_mode": "light", "light": "paper", "dark": "warm", "accent": "#1f6f50",
        "fonts": {"display": ("Newsreader", SERIF_FALLBACK), "body": ("Inter", SANS_FALLBACK), "mono": ("IBM Plex Mono", MONO_FALLBACK)},
        "display_weight": 500, "radius": (0, 2, 4), "elevation": "none", "section_pad": 128, "density": "low",
    },
}

SHADOWS = {
    "border": ("none", "0 1px 2px rgb(15 23 42 / 0.06)", "0 4px 12px rgb(15 23 42 / 0.08)"),
    "shadow": ("0 1px 2px rgb(15 23 42 / 0.06)", "0 1px 2px rgb(15 23 42 / 0.06), 0 8px 24px rgb(15 23 42 / 0.08)",
               "0 2px 4px rgb(15 23 42 / 0.06), 0 16px 40px rgb(15 23 42 / 0.12)"),
    "shadow-light": ("0 1px 2px rgb(26 24 20 / 0.05)", "0 2px 8px rgb(26 24 20 / 0.07)", "0 8px 28px rgb(26 24 20 / 0.10)"),
    "glow": ("inset 0 1px 0 rgb(255 255 255 / 0.04)", "inset 0 1px 0 rgb(255 255 255 / 0.06), 0 0 0 1px rgb(255 255 255 / 0.04)",
             "0 0 0 1px rgb(255 255 255 / 0.08), 0 8px 32px rgb(0 0 0 / 0.5)"),
    "none": ("none", "none", "none"),
}
SPACE = [0, 2, 4, 8, 12, 16, 24, 32, 40, 48, 64, 80, 96, 128, 160]  # px; Carbon-like 8px scale [CARBON]
TYPE = {  # fluid sizes: (min px, max px)
    "xs": (12, 12), "sm": (14, 14), "base": (16, 17), "lg": (18, 20), "xl": (20, 24),
    "2xl": (24, 30), "3xl": (30, 40), "4xl": (36, 52), "5xl": (44, 68),
}
MOTION = {
    "dur-instant": "100ms", "dur-fast": "150ms", "dur-base": "220ms", "dur-slow": "400ms", "dur-reveal": "600ms",
    "ease-out": "cubic-bezier(0, 0, 0.38, 0.9)", "ease-in": "cubic-bezier(0.2, 0, 1, 0.9)",
    "ease-standard": "cubic-bezier(0.2, 0, 0.38, 0.9)", "ease-expressive": "cubic-bezier(0.16, 1, 0.3, 1)",
}


def _fluid(lo, hi, vw_lo=375, vw_hi=1440):
    if lo == hi:
        return f"{lo / 16:g}rem"
    slope = (hi - lo) / (vw_hi - vw_lo)
    base = lo - slope * vw_lo
    return f"clamp({lo / 16:g}rem, {base / 16:.3f}rem + {slope * 100:.3f}vw, {hi / 16:g}rem)"


def palette(direction, mode, accent=None):
    d = DIRECTIONS[direction]
    n = dict((LIGHT_NEUTRALS if mode == "light" else DARK_NEUTRALS)[d[mode]])
    acc = accent or d["accent"]
    c.parse(acc)  # validate early
    # Button fill: keep hue; make sure light or dark text on it reaches 4.5:1.
    fill = c.to_hex(c.parse(acc))
    on = c.best_text_on(fill)
    if c.ratio(on, fill) < c.AA_NORMAL:
        fill = c.adjust_to(fill, on, c.AA_NORMAL)
    hover = c.adjust_to(fill, on, min(c.ratio(on, fill) + 1.2, 12))
    n.update({
        "accent": fill, "accent-hover": hover, "accent-contrast": on,
        # links and highlighted words must read on every page surface
        "accent-text": c.adjust_to(c.adjust_to(acc, n["bg"], 4.6), n["bg-subtle"], 4.5),
        "border-input": c.adjust_to(n["border-strong"], n["surface"], 3.0),
    })
    n["focus"] = c.adjust_to(n["accent-text"], n["bg"], 3.0)
    for k, v in STATUS[mode].items():
        n[k] = c.adjust_to(v, n["surface"], 4.5)
    return n


def build(direction, accent=None):
    if direction not in DIRECTIONS:
        raise KeyError(f"unknown direction {direction!r}; choose from {', '.join(DIRECTIONS)}")
    d = DIRECTIONS[direction]
    r1, r2, r3 = d["radius"]
    sh = SHADOWS[d["elevation"]]
    fonts = {k: f'"{name}", {fb}' for k, (name, fb) in d["fonts"].items()}
    families = sorted({name for name, _ in d["fonts"].values()})
    gf = "https://fonts.googleapis.com/css2?" + "&".join(
        f"family={f.replace(' ', '+')}:wght@400..700" for f in families) + "&display=swap"
    return {
        "direction": direction,
        "summary": d["summary"],
        "default_mode": d["default_mode"],
        "modes": {m: palette(direction, m, accent) for m in ("light", "dark")},
        "fonts": fonts,
        "font_url": gf,
        "display_weight": d["display_weight"],
        "radius": {"sm": f"{r1}px", "md": f"{r2}px", "lg": f"{r3}px", "pill": "999px"},
        "shadow": {"sm": sh[0], "md": sh[1], "lg": sh[2]},
        "space": {str(v): f"{v / 16:g}rem" for v in SPACE},  # named by px: --space-16 = 1rem
        "section_pad": f"{d['section_pad'] / 16:g}rem",
        "type": {k: _fluid(*v) for k, v in TYPE.items()},
        "motion": MOTION,
        "density": d["density"],
        "measure": "65ch",
    }


TEXT_PAIRS = [  # (foreground, background, minimum)
    ("text", "bg", 4.5), ("text", "bg-subtle", 4.5), ("text", "surface", 4.5),
    ("text-muted", "bg", 4.5), ("text-muted", "bg-subtle", 4.5), ("text-muted", "surface", 4.5),
    ("accent-text", "bg", 4.5), ("accent-text", "bg-subtle", 4.5), ("accent-contrast", "accent", 4.5),
    ("accent-contrast", "accent-hover", 4.5), ("focus", "bg", 3.0), ("border-input", "surface", 3.0),
    ("success", "surface", 4.5), ("warning", "surface", 4.5), ("danger", "surface", 4.5), ("info", "surface", 4.5),
]


def report(tokens):
    rows = []
    for mode, pal in tokens["modes"].items():
        for fg, bg, need in TEXT_PAIRS:
            r = c.ratio(pal[fg], pal[bg])
            rows.append({"mode": mode, "fg": fg, "bg": bg, "ratio": round(r, 2), "min": need, "pass": r >= need})
    return rows


def _vars(pal):
    return "\n".join(f"  --{k}: {v};" for k, v in pal.items())


def to_css(t):
    default, other = t["default_mode"], ("dark" if t["default_mode"] == "light" else "light")
    common = [f'  --font-display: {t["fonts"]["display"]};', f'  --font-body: {t["fonts"]["body"]};',
              f'  --font-mono: {t["fonts"]["mono"]};', f'  --display-weight: {t["display_weight"]};']
    common += [f"  --radius-{k}: {v};" for k, v in t["radius"].items()]
    common += [f"  --shadow-{k}: {v};" for k, v in t["shadow"].items()]
    common += [f"  --space-{k}: {v};" for k, v in t["space"].items()]
    common += [f"  --text-{k}: {v};" for k, v in t["type"].items()]
    common += [f"  --{k}: {v};" for k, v in t["motion"].items()]
    common += [f"  --section-pad: {t['section_pad']};", f"  --measure: {t['measure']};"]
    out = [f"/* {t['direction']} tokens: {t['summary']}",
           f"   Fonts: <link rel=\"stylesheet\" href=\"{t['font_url']}\"> */",
           ":root {", f"  color-scheme: {default};", "\n".join(common), _vars(t["modes"][default]), "}"]
    if default == "light":  # follow the OS, with a data-theme override either way
        out += ['@media (prefers-color-scheme: dark) {', '  :root:not([data-theme="light"]) {', "    color-scheme: dark;",
                "\n".join("  " + line for line in _vars(t["modes"]["dark"]).splitlines()), "  }", "}"]
    out += [f':root[data-theme="{other}"] {{', f"  color-scheme: {other};", _vars(t["modes"][other]), "}",
            f':root[data-theme="{default}"] {{', f"  color-scheme: {default};", _vars(t["modes"][default]), "}"]
    return "\n".join(out) + "\n"


def to_tailwind(t):
    keys = list(t["modes"]["light"].keys())
    cfg = {
        "darkMode": ["selector", '[data-theme="dark"]'],
        "theme": {"extend": {
            "colors": {k: f"var(--{k})" for k in keys},
            "fontFamily": {"display": ["var(--font-display)"], "sans": ["var(--font-body)"], "mono": ["var(--font-mono)"]},
            "borderRadius": {k: f"var(--radius-{k})" for k in t["radius"]},
            "boxShadow": {k: f"var(--shadow-{k})" for k in t["shadow"]},
            "fontSize": {k: f"var(--text-{k})" for k in t["type"]},
            "transitionDuration": {k[4:]: f"var(--{k})" for k in t["motion"] if k.startswith("dur-")},
            "transitionTimingFunction": {k[5:]: f"var(--{k})" for k in t["motion"] if k.startswith("ease-")},
            "maxWidth": {"measure": "var(--measure)"},
        }},
    }
    return ("// tailwind.config.js: the values point at CSS variables; include the CSS from\n"
            f"// `tokens.py {t['direction']} --format css` in your global stylesheet.\n"
            "module.exports = " + json.dumps(cfg, indent=2) + ";\n")


def main(argv=None):
    p = argparse.ArgumentParser(description="Design tokens for a B2B style direction.")
    p.add_argument("direction", nargs="?")
    p.add_argument("--accent")
    p.add_argument("--format", choices=["css", "json", "tailwind"], default="css")
    p.add_argument("--report", action="store_true", help="print the contrast report instead")
    p.add_argument("--list", action="store_true")
    a = p.parse_args(argv)
    if a.list or not a.direction:
        for k, d in DIRECTIONS.items():
            print(f"{k:14} {d['default_mode']:5}  {d['summary']}")
        return 0
    try:
        t = build(a.direction, a.accent)
    except (KeyError, c.ColorError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if a.report:
        rows = report(t)
        for r in rows:
            print(f"{'pass' if r['pass'] else 'FAIL'}  {r['mode']:5} {r['fg']:>15} on {r['bg']:<13} {r['ratio']:>5}:1  (min {r['min']})")
        return 0 if all(r["pass"] for r in rows) else 1
    print({"css": to_css, "tailwind": to_tailwind, "json": lambda t: json.dumps(t, indent=2)}[a.format](t), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
