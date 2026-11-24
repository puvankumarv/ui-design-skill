#!/usr/bin/env python3
"""Colour parsing and WCAG 2.2 contrast (standard library only).

Usage:  python3 contrast.py <foreground> <background>
        python3 contrast.py "#5b6470" white

Accepts #rgb, #rgba, #rrggbb, #rrggbbaa, rgb()/rgba() (comma or space syntax), hsl()/hsla(),
and a few names (white, black, transparent). Translucent colours are composited over the
background (or over white when the background itself is translucent).
"""
import colorsys
import re
import sys

NAMED = {"white": (255, 255, 255, 1.0), "black": (0, 0, 0, 1.0), "transparent": (0, 0, 0, 0.0)}
AA_NORMAL, AA_LARGE, AAA_NORMAL, AAA_LARGE = 4.5, 3.0, 7.0, 4.5


class ColorError(ValueError):
    pass


def _num(token, scale):
    token = token.strip()
    if token.endswith("%"):
        return float(token[:-1]) / 100 * scale
    return float(token)


def parse(value):
    """Return (r, g, b, a) with r/g/b 0-255 floats and a 0-1, or raise ColorError."""
    if value is None:
        raise ColorError("no colour")
    s = str(value).strip().lower()
    if s in NAMED:
        return NAMED[s]
    if s.startswith("#"):
        h = s[1:]
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        if len(h) not in (6, 8) or not re.fullmatch(r"[0-9a-f]+", h):
            raise ColorError(f"bad hex colour {value!r}")
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return (float(r), float(g), float(b), a)
    m = re.fullmatch(r"(rgba?|hsla?)\((.*)\)", s)
    if not m:
        raise ColorError(f"unsupported colour {value!r}")
    kind, body = m.group(1), m.group(2)
    parts = [p for p in re.split(r"[,\s/]+", body.strip()) if p]
    if len(parts) not in (3, 4):
        raise ColorError(f"bad colour {value!r}")
    alpha = _num(parts[3], 1.0) if len(parts) == 4 else 1.0
    try:
        if kind.startswith("rgb"):
            r, g, b = (_num(p, 255) for p in parts[:3])
        else:
            hue = float(parts[0].replace("deg", ""))
            sat, light = _num(parts[1], 1.0), _num(parts[2], 1.0)
            r, g, b = (c * 255 for c in colorsys.hls_to_rgb((hue % 360) / 360, light, sat))
    except ValueError:
        raise ColorError(f"bad colour {value!r}")
    clamp = lambda v: max(0.0, min(255.0, v))  # noqa: E731
    return (clamp(r), clamp(g), clamp(b), max(0.0, min(1.0, alpha)))


def composite(fg, bg):
    """Composite a possibly translucent fg over bg; returns an opaque (r, g, b, 1.0)."""
    if bg[3] < 1:
        bg = composite(bg, NAMED["white"])
    a = fg[3]
    return tuple(fg[i] * a + bg[i] * (1 - a) for i in range(3)) + (1.0,)


def luminance(rgb):
    def chan(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (chan(c) for c in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg, bg):
    """WCAG contrast ratio between two colours (strings or tuples)."""
    fg = parse(fg) if isinstance(fg, str) else fg
    bg = parse(bg) if isinstance(bg, str) else bg
    bg = composite(bg, NAMED["white"]) if bg[3] < 1 else bg
    fg = composite(fg, bg) if fg[3] < 1 else fg
    l1, l2 = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def levels(r):
    return {"ratio": round(r, 2), "aa_normal": r >= AA_NORMAL, "aa_large": r >= AA_LARGE,
            "aaa_normal": r >= AAA_NORMAL, "aaa_large": r >= AAA_LARGE, "ui_components": r >= AA_LARGE}


def to_hex(rgb):
    return "#" + "".join(f"{round(max(0, min(255, c))):02x}" for c in rgb[:3])


def adjust_to(color, bg, target=AA_NORMAL):
    """Keep the hue, move lightness until color reaches `target` contrast on bg. Returns hex.

    Moves away from the background's lightness (darker on light backgrounds, lighter on dark ones).
    Returns the input unchanged if it already passes."""
    c, b = parse(color), parse(bg)
    if ratio(c, b) >= target:
        return to_hex(c)
    h, l, s = colorsys.rgb_to_hls(*(v / 255 for v in c[:3]))
    darker = luminance(b) > 0.18
    step = -0.01 if darker else 0.01
    while 0 <= l <= 1:
        l += step
        cand = tuple(v * 255 for v in colorsys.hls_to_rgb(h, max(0, min(1, l)), s)) + (1.0,)
        if ratio(cand, b) >= target:
            return to_hex(cand)
    return "#000000" if darker else "#ffffff"


def best_text_on(bg, light="#ffffff", dark="#0b0d12"):
    """Whichever of a light or dark text colour has more contrast on bg."""
    return light if ratio(light, bg) >= ratio(dark, bg) else dark


def main(argv):
    if len(argv) != 3:
        print(__doc__.strip().splitlines()[2].strip())
        return 2
    try:
        r = ratio(argv[1], argv[2])
    except ColorError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    lv = levels(r)
    print(f"{argv[1]} on {argv[2]}: {lv['ratio']}:1")
    for k, label in (("aa_normal", "AA body text (4.5:1)"), ("aa_large", "AA large text / UI (3:1)"),
                     ("aaa_normal", "AAA body text (7:1)")):
        print(f"  {'pass' if lv[k] else 'FAIL'}  {label}")
    return 0 if lv["aa_normal"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
