"""Offline regression checks. Run: python -m unittest discover -s tests -v"""

import json
from email.message import EmailMessage
from pathlib import Path
import re
import tempfile
from threading import Thread
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import urlopen

from tools.build_fixtures import Document, Node, decode_text
from tools import preview


FIXTURES = Path(__file__).resolve().parent / "fixtures"


def nodes(node):
    yield node
    for child in node.children:
        if isinstance(child, Node):
            yield from nodes(child)


class FixtureContentTests(unittest.TestCase):
    def test_utf8_capture_without_a_mime_charset(self):
        message = EmailMessage()
        message["Content-Type"] = "text/html"
        message.set_payload("Pokémon « previous ».".encode("utf-8"))
        self.assertEqual(decode_text(message), "Pokémon « previous ».")

    def test_three_distinct_smf_page_types(self):
        manifest = json.loads((FIXTURES / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual([page["page"] for page in manifest["pages"]], ["index.html", "board.html", "topic.html"])
        for name in ("index", "board", "topic"):
            with self.subTest(page=name):
                all_nodes = list(nodes(Document((FIXTURES / (name + ".html")).read_text(encoding="utf-8")).root))
                self.assertTrue(any(n.tag == "body" and n.attrs.get("id") == "page_bg" for n in all_nodes))
                self.assertTrue(any(n.attrs.get("id") == "mainbody" for n in all_nodes))
                post_count = sum("post" in (n.attrs.get("class") or "").split() for n in all_nodes)
                if name == "topic":
                    self.assertGreaterEqual(post_count, 2, "Keep multiple posts to exercise author and signature panels")
                else:
                    self.assertEqual(post_count, 0)
                if name != "index":
                    self.assertTrue(any(n.attrs.get("id") == "quickModForm" for n in all_nodes))

    def test_captures_have_no_active_remote_content_or_session_controls(self):
        for path in FIXTURES.glob("*.html"):
            with self.subTest(page=path.name):
                source = path.read_text(encoding="utf-8")
                self.assertNotRegex(source, r"(?i)sesc=|PHPSESSID|session_id|session_var|cid:|--tig-bg|grammarly")
                self.assertNotIn("michaelplzno", source)
                self.assertNotIn("Martha's World", source)
                for node in nodes(Document(source).root):
                    self.assertNotIn(node.tag, {"script", "object", "embed", "base", "style"})
                    for key, value in node.attrs.items():
                        self.assertFalse(key.startswith("on"))
                        if key == "src" or (key == "href" and node.tag == "link"):
                            self.assertTrue(value.startswith("/fixtures/assets/"), value)
                            self.assertTrue((FIXTURES / value.removeprefix("/fixtures/")).is_file(), value)
                        if key == "href" and node.tag == "a":
                            self.assertTrue(value.startswith("#"), value)
                        if key == "action":
                            self.assertEqual(value, "#")
                    self.assertNotEqual((node.attrs.get("type") or "").lower(), "hidden")

    def test_legacy_css_uses_only_bundled_assets(self):
        for path in FIXTURES.rglob("*.css"):
            with self.subTest(css=path.name):
                source = path.read_text(encoding="utf-8")
                self.assertNotIn("--tig-", source, "An archived theme must never mask the current CSS")
                self.assertNotIn("@import", source)
                for target in re.findall(r'url\("([^"]+)"\)', source):
                    self.assertTrue(target.startswith("/fixtures/assets/"))
                    self.assertTrue((FIXTURES / target.removeprefix("/fixtures/")).is_file(), target)

    def test_archives_are_not_in_the_public_fixtures(self):
        self.assertFalse(list(FIXTURES.rglob("*.mhtml")))
        self.assertLess(sum(p.stat().st_size for p in FIXTURES.rglob("*") if p.is_file()), 1_000_000)


class PreviewServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = preview.PreviewServer(("127.0.0.1", 0), preview.Handler)
        cls.worker = Thread(target=cls.server.serve_forever, daemon=True)
        cls.worker.start()
        cls.base = "http://127.0.0.1:" + str(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.worker.join()

    def get(self, path):
        return urlopen(self.base + path, timeout=5)

    def test_theme_is_loaded_once_and_original_view_remains_available(self):
        for page in ("index", "board", "topic"):
            with self.subTest(page=page):
                with self.get("/fixtures/" + page + ".html") as response:
                    content = response.read().decode()
                    self.assertEqual(content.count('id="current-theme"'), 1)
                    self.assertIn("form-action 'none'", response.headers["Content-Security-Policy"])
                    self.assertIn("connect-src 'none'", response.headers["Content-Security-Policy"])
                    self.assertEqual(response.headers["Cache-Control"], "no-store")
                with self.get("/fixtures/" + page + ".html?theme=original") as response:
                    self.assertNotIn('id="current-theme"', response.read().decode())

    def test_theme_endpoint_reads_edits_without_a_rebuild(self):
        with tempfile.TemporaryDirectory() as directory:
            css_file = Path(directory) / "theme.user.css"
            with patch.object(preview, "THEME", css_file):
                for color in ("red", "blue"):
                    css_file.write_text('/* ==UserStyle==\n@name Test\n==/UserStyle== */\n'
                                        '@-moz-document url-prefix("https://forums.tigsource.com/") { '
                                        'body { color: ' + color + '; } }', encoding="utf-8")
                    with self.get("/theme.css") as response:
                        content = response.read().decode()
                        self.assertIn("color: " + color, content)
                        self.assertNotIn("@-moz-document", content)
                        self.assertNotIn("==UserStyle==", content)

    def test_real_theme_can_be_extracted(self):
        css = preview.theme_css()
        self.assertIn("--tig-bg", css)
        self.assertIn("@media", css)
        self.assertIn("data:image/svg+xml,", css)
        self.assertNotIn("@-moz-document", css)

    def test_files_outside_fixture_directory_are_not_served(self):
        for path in ("/README.md", "/fixtures/..%2f..%2fREADME.md", "/fixtures/assets/../../../../.git/config"):
            with self.subTest(path=path):
                with self.assertRaises(HTTPError) as caught:
                    self.get(path)
                self.assertEqual(caught.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
