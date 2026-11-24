#!/usr/bin/env python3
"""Page blueprints: section order with a default component for each (standard library only).

Usage:
  python3 blueprint.py <page> [--motion sales-led|self-serve|hybrid|service] [--enterprise] [--software]
                              [--no-logos] [--json]
  python3 blueprint.py --list

Data: templates/blueprints.json. Rationale: the page module named in the output.
"""
import argparse
import copy
import json
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "templates" / "blueprints.json"
MOTIONS = ("sales-led", "self-serve", "hybrid", "service")
PRIMARY_CTA = {
    "sales-led": ("Get a demo", "See how it works"),
    "self-serve": ("Start for free", "Book a demo"),
    "hybrid": ("Get started", "Get a demo"),
    "service": ("Request a quote", "Talk to an expert"),
}


def pages():
    return json.loads(DATA.read_text())["pages"]


def build(page, motion="hybrid", enterprise=False, software=True, logos=True):
    all_pages = pages()
    if page not in all_pages:
        raise KeyError(f"unknown page {page!r}; choose from {', '.join(all_pages)}")
    if motion not in MOTIONS:
        raise KeyError(f"unknown motion {motion!r}; choose from {', '.join(MOTIONS)}")
    bp = copy.deepcopy(all_pages[page])
    rules = bp.get("motions", {}).get(motion, {})
    sections = [s for s in bp["sections"] if s["id"] not in rules.get("remove", [])]
    for anchor, extra in rules.get("add_after", {}).items():
        idx = next((i for i, s in enumerate(sections) if s["id"] == anchor), len(sections) - 1)
        sections[idx + 1:idx + 1] = extra
    forced = set(rules.get("require", []))
    out = []
    for s in sections:
        req = s.get("required")
        if s["id"] in forced:
            req = True
        elif req == "enterprise":
            req = enterprise
        elif req == "software":
            req = software
        elif req == "if-logos":
            req = logos
            if not logos:
                continue
        out.append({**s, "required": bool(req)})
    primary, secondary = PRIMARY_CTA[motion]
    return {
        "page": page, "motion": motion, "module": bp["module"],
        "thin_evidence": bool(bp.get("thin_evidence")),
        "primary_cta": primary, "secondary_cta": secondary,
        "note": rules.get("note", ""),
        "sections": out,
    }


def to_text(b):
    lines = [f"# {b['page']} blueprint ({b['motion']})", f"Module: {b['module']}",
             f"Primary CTA: \"{b['primary_cta']}\"   Secondary: \"{b['secondary_cta']}\""]
    if b["thin_evidence"]:
        lines.append("Thin evidence: study 3-5 sites from the client's industry first and tell the user.")
    if b["note"]:
        lines.append(f"Note: {b['note']}")
    lines.append("")
    for i, s in enumerate(b["sections"], 1):
        flag = "required" if s["required"] else "optional"
        lines.append(f"{i:>2}. {s['id']:<18} [{flag}] {s['component']}")
        for alt in s.get("alternatives", []):
            lines.append(f"    {'':<18}  or: {alt}")
        if s.get("evidence"):
            lines.append(f"    {'':<18}  evidence: {s['evidence']}")
    return "\n".join(lines) + "\n"


def main(argv=None):
    p = argparse.ArgumentParser(description="Section order for a B2B page.")
    p.add_argument("page", nargs="?")
    p.add_argument("--motion", default="hybrid", choices=MOTIONS)
    p.add_argument("--enterprise", action="store_true", help="enterprise / regulated buyers: security required")
    p.add_argument("--no-software", action="store_true", help="not a software product: integrations optional")
    p.add_argument("--no-logos", action="store_true", help="no customer logos available yet")
    p.add_argument("--json", action="store_true")
    p.add_argument("--list", action="store_true")
    a = p.parse_args(argv)
    if a.list or not a.page:
        print("\n".join(pages()))
        return 0
    try:
        b = build(a.page, a.motion, a.enterprise, not a.no_software, not a.no_logos)
    except KeyError as e:
        print(f"error: {e.args[0]}", file=sys.stderr)
        return 2
    print(json.dumps(b, indent=2) if a.json else to_text(b), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
