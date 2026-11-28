#!/usr/bin/env python3
"""MCP server for the B2B UI Designer (stdio, standard library only).

Run:  python3 mcp_server.py

Tools:
  check_page        accessibility, modern-web, motion, B2B conversion and AI-slop checks on HTML (structured)
  design_tokens     tokens for a style direction as CSS, JSON or Tailwind, with a contrast report
  contrast          WCAG contrast ratio and pass levels for two colours (structured)
  page_blueprint    section order with a default component and evidence for each (structured)
  list_references   the skill's reference files, templates and examples
  read_reference    read one of those files

Resources: every reference, template and example as b2b://skill/<path>, plus a template for
completing paths. Prompts: design_page and audit_page, which clients like Claude Code show as
slash commands. Completions for prompt arguments and resource paths.

Protocol: dual-era, like the Residential Space Designer server. Legacy clients (2025-11-25 and
earlier) open with initialize; modern clients (2026-07-28) send per-request _meta and may probe
with server/discover. JSON-RPC 2.0 over stdin/stdout, one message per line. Logs go to stderr only.
"""
import base64
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
sys.path.insert(0, str(HERE))
import blueprint as bp  # noqa: E402
import check_page as cp  # noqa: E402
import contrast as ct  # noqa: E402
import tokens as tk  # noqa: E402

VERSION = "0.2.0"  # kept equal to .claude-plugin/plugin.json by the tests
MODERN = ["2026-07-28"]
LEGACY = ["2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05"]
META_VERSION = "io.modelcontextprotocol/protocolVersion"
READABLE_DIRS = ("references", "templates", "examples")
READABLE_SUFFIXES = (".md", ".json", ".html")
URI_PREFIX = "b2b://skill/"
CACHE = {"ttlMs": 3600000, "cacheScope": "public"}
MAX_HTML = 2_000_000

ICON = ("data:image/svg+xml;base64," + base64.b64encode(
    b"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='7' fill='#1d4ed8'/>"
    b"<rect x='7' y='8' width='18' height='4' rx='1' fill='#fff'/><rect x='7' y='15' width='8' height='9' rx='1' fill='#fff'/>"
    b"<rect x='17' y='15' width='8' height='9' rx='1' fill='#fff' opacity='.6'/></svg>").decode())
SERVER_INFO = {
    "name": "b2b-ui-designer", "version": VERSION, "title": "B2B UI Designer",
    "description": "Plan, tokenise, build and check B2B websites and product UI without AI slop.",
    "websiteUrl": "https://github.com/puvankumarv/ui-design-skill",
    "icons": [{"src": ICON, "mimeType": "image/svg+xml", "sizes": ["any"]}],
}
CAPABILITIES = {
    "tools": {"listChanged": False},
    "resources": {"subscribe": False, "listChanged": False},
    "prompts": {"listChanged": False},
    "completions": {},
}
INSTRUCTIONS = (
    "Tools for designing B2B pages. Get the section order from page_blueprint, generate design tokens with "
    "design_tokens, build the page, then run check_page until it has no errors and every warning is reviewed. "
    "check_page also flags generic AI-slop patterns. Use contrast for quick colour checks. Design guidance "
    "(page modules, components, cards, styles, motion, accessibility, modern web, AI slop, copy) is in the "
    "references: resources b2b://skill/..., or list_references / read_reference."
)

PAGES = list(bp.pages())
DIRECTIONS = list(tk.DIRECTIONS)
READ_ONLY = {"readOnlyHint": True, "idempotentHint": True, "openWorldHint": False}
FINDINGS = {"type": "array", "items": {"type": "object", "properties": {
    "rule": {"type": "string"}, "message": {"type": "string"}, "where": {"type": "string"}}}}

TOOLS = [
    {
        "name": "check_page",
        "title": "Check a B2B page",
        "description": (
            "Check an HTML page (with its <style> blocks and style attributes) for WCAG 2.2 AA problems "
            "(contrast, labels, names, alt text, focus, target size), semantic HTML, Core Web Vitals hygiene "
            "(image sizing and loading, fonts, blocking scripts), modern CSS, motion (reduced motion, pause "
            "controls, timing), B2B structure and conversion (sections, primary CTA, proof before the ask, "
            "pricing units, forms) and generic AI-slop patterns (purple gradients, gradient text, default "
            "framework colours, emoji icons, buzzwords, unsourced stats, fake testimonials). Returns errors "
            "(must fix), warnings (review) and ok. Mark sections with data-section and the primary CTA with "
            "data-cta=\"primary\" for the structure rules."
        ),
        "inputSchema": {"type": "object", "properties": {
            "html": {"type": "string", "description": "The full HTML document."}}, "required": ["html"]},
        "outputSchema": {"type": "object", "properties": {
            "ok": {"type": "boolean"}, "errors": FINDINGS, "warnings": FINDINGS,
            "sections": {"type": "array", "items": {"type": "string"}}, "summary": {"type": "object"}},
            "required": ["ok", "errors", "warnings"]},
        "annotations": READ_ONLY,
    },
    {
        "name": "design_tokens",
        "title": "Generate design tokens",
        "description": (
            "Design tokens for a B2B style direction: colours for light and dark mode, fonts, radius, shadows, "
            "spacing, fluid type and motion. An optional brand accent keeps its hue; its lightness is adjusted "
            "so button text, links and the focus ring pass WCAG contrast. Returns the tokens in the chosen "
            "format plus a contrast report for every text/background pair."
        ),
        "inputSchema": {"type": "object", "properties": {
            "direction": {"type": "string", "enum": DIRECTIONS,
                          "description": "enterprise, modern-saas, fintech-trust, developer or editorial (see references/styles.md)."},
            "accent": {"type": "string", "description": "Optional brand accent colour, e.g. #0f766e."},
            "format": {"type": "string", "enum": ["css", "json", "tailwind"], "default": "css"}},
            "required": ["direction"]},
        "annotations": READ_ONLY,
    },
    {
        "name": "contrast",
        "title": "Contrast ratio",
        "description": "WCAG 2.2 contrast ratio between a text colour and a background, with AA/AAA pass levels. "
                       "Accepts hex, rgb(), hsl() and white/black; translucent colours are composited.",
        "inputSchema": {"type": "object", "properties": {
            "foreground": {"type": "string"}, "background": {"type": "string"}},
            "required": ["foreground", "background"]},
        "outputSchema": {"type": "object", "properties": {
            "ratio": {"type": "number"}, "aa_normal": {"type": "boolean"}, "aa_large": {"type": "boolean"},
            "aaa_normal": {"type": "boolean"}, "aaa_large": {"type": "boolean"}, "ui_components": {"type": "boolean"}},
            "required": ["ratio", "aa_normal", "aa_large"]},
        "annotations": READ_ONLY,
    },
    {
        "name": "page_blueprint",
        "title": "Page blueprint",
        "description": (
            "Section order for a B2B page type and sales motion, with the data-section id, whether it's required, "
            "a default component, alternatives and the evidence behind it. Also returns the primary and secondary "
            "CTA labels for the motion and the page module to read."
        ),
        "inputSchema": {"type": "object", "properties": {
            "page": {"type": "string", "enum": PAGES},
            "motion": {"type": "string", "enum": list(bp.MOTIONS), "default": "hybrid"},
            "enterprise": {"type": "boolean", "default": False, "description": "Enterprise or regulated buyers (security required)."},
            "software": {"type": "boolean", "default": True, "description": "A software product (integrations required)."},
            "logos": {"type": "boolean", "default": True, "description": "Customer logos are available."}},
            "required": ["page"]},
        "outputSchema": {"type": "object", "properties": {
            "page": {"type": "string"}, "motion": {"type": "string"}, "module": {"type": "string"},
            "primary_cta": {"type": "string"}, "secondary_cta": {"type": "string"},
            "thin_evidence": {"type": "boolean"}, "note": {"type": "string"},
            "sections": {"type": "array", "items": {"type": "object"}}},
            "required": ["page", "sections", "primary_cta"]},
        "annotations": READ_ONLY,
    },
    {
        "name": "list_references",
        "title": "List skill references",
        "description": "List the skill's reference files (page modules, components, cards, styles, motion, "
                       "accessibility, modern web, AI slop, copy, sources), templates and example pages.",
        "inputSchema": {"type": "object", "properties": {}},
        "annotations": READ_ONLY,
    },
    {
        "name": "read_reference",
        "title": "Read a skill reference",
        "description": "Read one file returned by list_references, e.g. references/ai-slop.md.",
        "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]},
        "annotations": READ_ONLY,
    },
]

PROMPTS = [
    {
        "name": "design_page",
        "title": "Design a B2B page",
        "description": "Plan, tokenise, build and check a B2B page from a brief.",
        "arguments": [
            {"name": "page", "description": f"Page type: {', '.join(PAGES)}", "required": True},
            {"name": "brief", "description": "Product, buyer, what the page must achieve", "required": True},
            {"name": "motion", "description": "sales-led, self-serve, hybrid or service", "required": False},
            {"name": "style", "description": f"Style direction: {', '.join(DIRECTIONS)}", "required": False},
        ],
    },
    {
        "name": "audit_page",
        "title": "Audit a B2B page",
        "description": "Review an existing page: accessibility, modern web, AI slop and conversion.",
        "arguments": [{"name": "page", "description": "A URL, or the page's HTML", "required": True}],
    },
]


class ToolError(Exception):
    """A problem with the tool's input, reported back to the model as isError."""


class RpcError(Exception):
    def __init__(self, code, message, data=None):
        super().__init__(message)
        self.code, self.data = code, data


# ---------------------------------------------------------------- helpers

def _readable():
    files = []
    for d in READABLE_DIRS:
        files += [p for p in sorted((SKILL / d).rglob("*")) if p.is_file() and p.suffix in READABLE_SUFFIXES]
    return files


def _rel(p):
    return p.relative_to(SKILL).as_posix()


def _read_rel(rel):
    rel = str(rel or "").strip().lstrip("/")
    target = (SKILL / rel).resolve()
    if target not in {p.resolve() for p in _readable()}:
        return None
    return target


def _mime(p):
    return {".json": "application/json", ".html": "text/html"}.get(p.suffix, "text/markdown")


def _title(p):
    if p.suffix == ".md":
        for line in p.read_text().splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    return p.stem.replace("-", " ").replace("_", " ").capitalize()


def structured(data):
    return {"content": [{"type": "text", "text": json.dumps(data, ensure_ascii=False, indent=2)}], "structuredContent": data}


def text(t):
    return {"content": [{"type": "text", "text": t}]}


def _str(args, key, required=True):
    v = args.get(key)
    if v is None and not required:
        return None
    if not isinstance(v, str) or not v.strip():
        raise ToolError(f"{key} must be a non-empty string")
    return v


# ---------------------------------------------------------------- tools

def check_page(args):
    html = _str(args, "html")
    if len(html) > MAX_HTML:
        raise ToolError(f"html is larger than {MAX_HTML} characters")
    return structured(cp.check(html))


def design_tokens(args):
    direction = _str(args, "direction")
    fmt = args.get("format", "css")
    if fmt not in ("css", "json", "tailwind"):
        raise ToolError("format must be css, json or tailwind")
    try:
        t = tk.build(direction, _str(args, "accent", required=False))
    except KeyError as e:
        raise ToolError(e.args[0])
    except ct.ColorError as e:
        raise ToolError(f"accent: {e}")
    rows = tk.report(t)
    body = {"css": tk.to_css, "tailwind": tk.to_tailwind, "json": lambda x: json.dumps(x, indent=2)}[fmt](t)
    failing = [r for r in rows if not r["pass"]]
    summary = (f"Contrast: all {len(rows)} pairs pass." if not failing else
               "Contrast failures: " + "; ".join(f"{r['mode']} {r['fg']} on {r['bg']} {r['ratio']}:1" for r in failing))
    return {"content": [{"type": "text", "text": body}, {"type": "text", "text": summary + f"\nFonts: {t['font_url']}"}],
            "structuredContent": {"direction": direction, "format": fmt, "font_url": t["font_url"], "contrast": rows}}


def contrast(args):
    try:
        return structured(ct.levels(ct.ratio(_str(args, "foreground"), _str(args, "background"))))
    except ct.ColorError as e:
        raise ToolError(str(e))


def page_blueprint(args):
    page = _str(args, "page")
    flags = {}
    for k, default in (("enterprise", False), ("software", True), ("logos", True)):
        v = args.get(k, default)
        if not isinstance(v, bool):
            raise ToolError(f"{k} must be true or false")
        flags[k] = v
    try:
        return structured(bp.build(page, args.get("motion", "hybrid"), **flags))
    except KeyError as e:
        raise ToolError(e.args[0])


def list_references(args):
    lines = [_rel(p) for p in _readable()]
    return text("Files you can pass to read_reference (also resources at b2b://skill/<path>):\n" + "\n".join(lines))


def read_reference(args):
    target = _read_rel(args.get("path"))
    if target is None:
        raise ToolError(f"{args.get('path')!r} is not a readable reference; call list_references for the list")
    return text(target.read_text())


HANDLERS = {
    "check_page": check_page,
    "design_tokens": design_tokens,
    "contrast": contrast,
    "page_blueprint": page_blueprint,
    "list_references": list_references,
    "read_reference": read_reference,
}


# ---------------------------------------------------------------- resources, prompts, completions

def resources_list(params, modern):
    return {"resources": [{"uri": URI_PREFIX + _rel(p), "name": _rel(p), "title": _title(p),
                           "mimeType": _mime(p), "size": p.stat().st_size} for p in _readable()]}


def resource_templates(params, modern):
    return {"resourceTemplates": [{
        "uriTemplate": URI_PREFIX + "{path}", "name": "skill-file", "title": "Skill reference, template or example",
        "description": "Any file under references/, templates/ or examples/, e.g. b2b://skill/references/ai-slop.md",
    }]}


def resources_read(params, modern):
    uri = str(params.get("uri", ""))
    target = _read_rel(uri[len(URI_PREFIX):]) if uri.startswith(URI_PREFIX) else None
    if target is None:
        raise RpcError(-32602 if modern else -32002, "Resource not found", {"uri": uri})
    return {"contents": [{"uri": uri, "mimeType": _mime(target), "text": target.read_text()}]}


def _embedded(rel):
    p = SKILL / rel
    return {"role": "user", "content": {"type": "resource", "resource": {
        "uri": URI_PREFIX + rel, "mimeType": _mime(p), "text": p.read_text()}}}


def prompts_get(params, modern):
    name, args = params.get("name"), params.get("arguments") or {}
    if name == "design_page":
        page, brief = str(args.get("page", "")).strip(), str(args.get("brief", "")).strip()
        if page not in PAGES or not brief:
            raise RpcError(-32602, f"design_page needs page (one of {', '.join(PAGES)}) and brief")
        motion = str(args.get("motion", "")).strip()
        style = str(args.get("style", "")).strip()
        lines = [f"Design a B2B {page.replace('-', ' ')} page.", f"Brief: {brief}"]
        if motion:
            lines.append(f"Sales motion: {motion}.")
        if style:
            lines.append(f"Style direction: {style}.")
        lines += [
            "",
            "Work like this:",
            "1. Read the page module attached here. Ask me only for what is missing and essential (max 5 questions).",
            "2. Get the section order from page_blueprint and write a page plan: each section, its component and why.",
            "3. Generate tokens with design_tokens (with my brand accent if I gave one).",
            "4. Build the page as one HTML file. Mark sections with data-section and the primary CTA with data-cta=\"primary\".",
            "5. Remove AI slop using the attached list. Never invent logos, quotes, numbers or certifications; use labelled placeholders.",
            "6. Run check_page. Fix every error and review every warning.",
            "7. Finish with the page plan, the page, the checker result and the list of placeholders I must replace.",
        ]
        msgs = [{"role": "user", "content": {"type": "text", "text": "\n".join(lines)}}]
        module = bp.pages()[page]["module"]
        for rel in (module, "references/ai-slop.md", "references/components.md"):
            if (SKILL / rel).exists():
                msgs.append(_embedded(rel))
        return {"description": f"Design a {page} page", "messages": msgs}
    if name == "audit_page":
        page = str(args.get("page", "")).strip()
        if not page:
            raise RpcError(-32602, "audit_page needs page (a URL or HTML)")
        how = ("Open the URL in a browser, record the section order, CTAs, proof and motion, and get the HTML if you can."
               if page.startswith(("http://", "https://")) else "The HTML is below.")
        msgs = [{"role": "user", "content": {"type": "text", "text": (
            "Audit this B2B page. " + how + " Run check_page on the HTML. Report, in this order: accessibility "
            "errors, modern-web and performance issues, AI-slop patterns, B2B structure and conversion issues "
            "(compare with page_blueprint for the page type), then style suggestions. For each finding say where it "
            "is, why it matters and the fix. End with the three changes that would help most.\n\n" + page)}},
            _embedded("references/ai-slop.md"), _embedded("references/modern-web.md")]
        return {"description": "Audit a B2B page", "messages": msgs}
    raise RpcError(-32602, f"Unknown prompt: {name}")


def complete(params, modern):
    ref, arg = params.get("ref") or {}, params.get("argument") or {}
    value = str(arg.get("value", "")).lower()
    options = []
    if ref.get("type") == "ref/prompt" and ref.get("name") == "design_page":
        options = {"page": PAGES, "motion": list(bp.MOTIONS), "style": DIRECTIONS}.get(arg.get("name"), [])
    elif ref.get("type") == "ref/resource" and ref.get("uri") == URI_PREFIX + "{path}" and arg.get("name") == "path":
        options = [_rel(p) for p in _readable()]
    hits = [o for o in options if value in o.lower()]
    hits.sort(key=lambda o: (not o.lower().startswith(value), o))
    return {"completion": {"values": hits[:100], "total": len(hits), "hasMore": len(hits) > 100}}


# ---------------------------------------------------------------- dispatch

def _call_tool(params, modern):
    name = params.get("name")
    if name not in HANDLERS:
        raise RpcError(-32602, f"Unknown tool: {name}")
    args = params.get("arguments") or {}
    if not isinstance(args, dict):
        return {**text("arguments must be an object"), "isError": True}
    try:
        return {**HANDLERS[name](args), "isError": False}
    except ToolError as e:
        return {**text(str(e)), "isError": True}


METHODS = {
    "tools/list": lambda p, m: {"tools": TOOLS},
    "tools/call": _call_tool,
    "resources/list": resources_list,
    "resources/templates/list": resource_templates,
    "resources/read": resources_read,
    "prompts/list": lambda p, m: {"prompts": PROMPTS},
    "prompts/get": prompts_get,
    "completion/complete": complete,
}
CACHEABLE = {"tools/list", "prompts/list", "resources/list", "resources/read", "resources/templates/list"}


def handle(msg):
    """Return the response dict for one JSON-RPC message, or None for notifications."""
    method, mid = msg.get("method"), msg.get("id")
    params = msg.get("params") if isinstance(msg.get("params"), dict) else {}
    if mid is None:
        return None
    meta = params.get("_meta") if isinstance(params.get("_meta"), dict) else {}
    asked = meta.get(META_VERSION)
    modern = asked is not None

    def ok(result):
        if modern:
            result = {**result, "resultType": "complete",
                      "_meta": {**result.get("_meta", {}), "io.modelcontextprotocol/serverInfo": SERVER_INFO}}
            if method in CACHEABLE:
                result.update(CACHE)
        return {"jsonrpc": "2.0", "id": mid, "result": result}

    def err(code, message, data=None):
        e = {"code": code, "message": message}
        if data is not None:
            e["data"] = data
        return {"jsonrpc": "2.0", "id": mid, "error": e}

    if modern and asked not in MODERN + LEGACY:
        return err(-32022, "Unsupported protocol version", {"supported": MODERN + LEGACY, "requested": asked})
    if method == "server/discover":
        return ok({"supportedVersions": MODERN + LEGACY, "capabilities": CAPABILITIES,
                   "_meta": {"io.modelcontextprotocol/serverInfo": SERVER_INFO},
                   "instructions": INSTRUCTIONS, **CACHE})
    if method == "initialize":
        version = params.get("protocolVersion")
        return ok({"protocolVersion": version if version in LEGACY else LEGACY[0], "capabilities": CAPABILITIES,
                   "serverInfo": SERVER_INFO, "instructions": INSTRUCTIONS})
    if method == "ping":
        return ok({})
    if method in METHODS:
        try:
            return ok(METHODS[method](params, modern))
        except RpcError as e:
            return err(e.code, str(e), e.data)
    return err(-32601, f"Method not found: {method}")


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            reply = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}
        else:
            try:
                reply = handle(msg) if isinstance(msg, dict) else {
                    "jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Invalid request"}}
            except Exception as e:  # keep the server alive; report the failure to the client
                print(f"internal error: {e!r}", file=sys.stderr)
                reply = {"jsonrpc": "2.0", "id": msg.get("id"), "error": {"code": -32603, "message": "Internal error"}}
        if reply is not None:
            sys.stdout.write(json.dumps(reply, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
