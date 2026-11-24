import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "b2b-ui-designer"
sys.path.insert(0, str(SKILL / "scripts"))
import mcp_server as srv  # noqa: E402

MODERN_META = {"io.modelcontextprotocol/protocolVersion": "2026-07-28"}


def call(method, params=None, mid=1):
    return srv.handle({"jsonrpc": "2.0", "id": mid, "method": method, "params": params or {}})


def tool(name, args, modern=False):
    params = {"name": name, "arguments": args}
    if modern:
        params["_meta"] = MODERN_META
    return call("tools/call", params)["result"]


class Protocol(unittest.TestCase):
    def test_initialize_legacy(self):
        r = call("initialize", {"protocolVersion": "2025-06-18"})["result"]
        self.assertEqual(r["protocolVersion"], "2025-06-18")
        self.assertEqual(r["serverInfo"]["name"], "b2b-ui-designer")
        self.assertEqual(call("initialize", {"protocolVersion": "1999-01-01"})["result"]["protocolVersion"], srv.LEGACY[0])

    def test_discover_and_modern_meta(self):
        r = call("server/discover", {"_meta": MODERN_META})["result"]
        self.assertIn("2026-07-28", r["supportedVersions"])
        lst = call("tools/list", {"_meta": MODERN_META})["result"]
        self.assertEqual(lst["resultType"], "complete")
        self.assertIn("ttlMs", lst)

    def test_unsupported_modern_version(self):
        r = call("tools/list", {"_meta": {"io.modelcontextprotocol/protocolVersion": "2099-01-01"}})
        self.assertEqual(r["error"]["code"], -32022)

    def test_notification_and_unknown(self):
        self.assertIsNone(srv.handle({"jsonrpc": "2.0", "method": "notifications/initialized"}))
        self.assertEqual(call("nope")["error"]["code"], -32601)
        self.assertEqual(call("tools/call", {"name": "nope"})["error"]["code"], -32602)

    def test_version_matches_plugin(self):
        plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        self.assertEqual(plugin["version"], srv.VERSION)
        self.assertIn("b2b-ui-designer/scripts/mcp_server.py", plugin["mcpServers"]["b2b-ui-designer"]["args"][0])

    def test_stdio_roundtrip(self):
        msgs = [{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-11-25"}},
                {"jsonrpc": "2.0", "method": "notifications/initialized"},
                {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}]
        out = subprocess.run([sys.executable, str(SKILL / "scripts" / "mcp_server.py")],
                             input="\n".join(json.dumps(m) for m in msgs) + "\nnot json\n",
                             capture_output=True, text=True, timeout=30)
        lines = [json.loads(x) for x in out.stdout.splitlines()]
        self.assertEqual([x.get("id") for x in lines], [1, 2, None])
        self.assertEqual(lines[2]["error"]["code"], -32700)


class Tools(unittest.TestCase):
    def test_tool_list(self):
        names = {t["name"] for t in call("tools/list")["result"]["tools"]}
        self.assertEqual(names, set(srv.HANDLERS))

    def test_check_page(self):
        html = (SKILL / "examples" / "saas-homepage.html").read_text()
        r = tool("check_page", {"html": html})
        self.assertFalse(r["isError"])
        self.assertTrue(r["structuredContent"]["ok"])
        bad = tool("check_page", {"html": "<p>x</p>"})
        self.assertFalse(bad["structuredContent"]["ok"])
        self.assertTrue(tool("check_page", {})["isError"])

    def test_design_tokens(self):
        r = tool("design_tokens", {"direction": "developer", "accent": "#22d3ee", "format": "css"})
        self.assertFalse(r["isError"])
        self.assertIn("--accent:", r["content"][0]["text"])
        self.assertTrue(all(row["pass"] for row in r["structuredContent"]["contrast"]))
        self.assertTrue(tool("design_tokens", {"direction": "nope"})["isError"])
        self.assertTrue(tool("design_tokens", {"direction": "enterprise", "accent": "zzz"})["isError"])

    def test_contrast(self):
        r = tool("contrast", {"foreground": "#000", "background": "#fff"}, modern=True)
        self.assertEqual(r["structuredContent"]["ratio"], 21.0)
        self.assertTrue(tool("contrast", {"foreground": "x", "background": "#fff"})["isError"])

    def test_blueprint(self):
        r = tool("page_blueprint", {"page": "pricing", "motion": "self-serve"})
        self.assertEqual(r["structuredContent"]["primary_cta"], "Start for free")
        self.assertTrue(tool("page_blueprint", {"page": "nope"})["isError"])
        self.assertTrue(tool("page_blueprint", {"page": "homepage", "enterprise": "yes"})["isError"])

    def test_references(self):
        listing = tool("list_references", {})["content"][0]["text"]
        self.assertIn("references/ai-slop.md", listing)
        self.assertIn("# AI slop", tool("read_reference", {"path": "references/ai-slop.md"})["content"][0]["text"])
        self.assertTrue(tool("read_reference", {"path": "../README.md"})["isError"])
        self.assertTrue(tool("read_reference", {"path": "scripts/check_page.py"})["isError"])


class ResourcesPrompts(unittest.TestCase):
    def test_resources(self):
        res = call("resources/list")["result"]["resources"]
        uris = {r["uri"] for r in res}
        self.assertIn("b2b://skill/references/modern-web.md", uris)
        read = call("resources/read", {"uri": "b2b://skill/references/modern-web.md"})["result"]
        self.assertIn("Core Web Vitals", read["contents"][0]["text"])
        self.assertEqual(call("resources/read", {"uri": "b2b://skill/x"})["error"]["code"], -32002)
        self.assertEqual(call("resources/read", {"uri": "b2b://skill/x", "_meta": MODERN_META})["error"]["code"], -32602)

    def test_prompts(self):
        names = {p["name"] for p in call("prompts/list")["result"]["prompts"]}
        self.assertEqual(names, {"design_page", "audit_page"})
        r = call("prompts/get", {"name": "design_page", "arguments": {"page": "homepage", "brief": "payroll for SMBs"}})["result"]
        uris = [m["content"]["resource"]["uri"] for m in r["messages"][1:]]
        self.assertIn("b2b://skill/references/pages/homepage.md", uris)
        self.assertIn("b2b://skill/references/ai-slop.md", uris)
        self.assertEqual(call("prompts/get", {"name": "design_page", "arguments": {"page": "x"}})["error"]["code"], -32602)
        audit = call("prompts/get", {"name": "audit_page", "arguments": {"page": "https://example.com"}})["result"]
        self.assertIn("browser", audit["messages"][0]["content"]["text"])

    def test_completions(self):
        r = call("completion/complete", {"ref": {"type": "ref/prompt", "name": "design_page"},
                                         "argument": {"name": "style", "value": "dev"}})["result"]
        self.assertEqual(r["completion"]["values"], ["developer"])
        r = call("completion/complete", {"ref": {"type": "ref/resource", "uri": "b2b://skill/{path}"},
                                         "argument": {"name": "path", "value": "slop"}})["result"]
        self.assertIn("references/ai-slop.md", r["completion"]["values"])


class SkillPackage(unittest.TestCase):
    def test_frontmatter(self):
        text = (SKILL / "SKILL.md").read_text()
        m = re.match(r"---\nname: (.+)\ndescription: (.+)\n---\n", text)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), "b2b-ui-designer")
        self.assertLessEqual(len(m.group(2)), 1024)

    def test_referenced_files_exist(self):
        text = (SKILL / "SKILL.md").read_text()
        paths = set(re.findall(r"`((?:references|templates|scripts)/[\w./-]+\.(?:md|json|py))`", text))
        self.assertTrue(paths)
        for p in paths:
            self.assertTrue((SKILL / p).exists(), p)
        for name in re.findall(r"`([\w-]+\.md)`", text.split("Shared references")[1].split("\n")[0]):
            self.assertTrue((SKILL / "references" / name).exists(), name)

    def test_readme_paths_exist(self):
        for p in re.findall(r"`(b2b-ui-designer/[\w./-]+)`", (ROOT / "README.md").read_text()):
            self.assertTrue((ROOT / p).exists(), p)


if __name__ == "__main__":
    unittest.main()
