"""Serve the offline fixtures with the current UserCSS. Run: python tools/preview.py"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import argparse
from html import escape
import mimetypes
from pathlib import Path
import re
import socket
from urllib.parse import parse_qs, unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
THEME = ROOT / "tigsource-midnight-grid.user.css"
CSP = ("default-src 'none'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
       "frame-src 'self'; base-uri 'none'; form-action 'none'; connect-src 'none'")


def theme_css():
    source = THEME.read_text(encoding="utf-8")
    source = re.sub(r"\A\s*/\*\s*==UserStyle==.*?==/UserStyle==\s*\*/", "", source, count=1, flags=re.S)
    match = re.fullmatch(r'\s*@-moz-document\s+url-prefix\("https://forums\.tigsource\.com/"\)\s*\{(.*)\}\s*', source, re.S)
    if not match:
        raise ValueError("Expected one TIGSource-scoped UserCSS block; update the preview extractor if the scope changes")
    return match.group(1)


class PreviewServer(ThreadingHTTPServer):
    # In particular, do not let Windows share an already occupied port with a
    # different application merely because HTTPServer enables SO_REUSEADDR.
    allow_reuse_address = False

    def server_bind(self):
        if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        super().server_bind()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        route = urlsplit(self.path)
        path = unquote(route.path)
        if path == "/":
            links = "".join(f'<li>{escape(label)}: <a href="/fixtures/{name}.html">current theme</a> | '
                            f'<a href="/fixtures/{name}.html?theme=original">original skin</a></li>'
                            for name, label in [("index", "Forum index"), ("board", "Townhall board"), ("topic", "Neofeud topic")])
            return self.respond(("<!doctype html><meta charset=utf-8><title>Midnight Grid fixtures</title>"
                                 "<h1>Midnight Grid layout fixtures</h1><p>Offline, anonymized captures. "
                                 "The current theme file is reread on each refresh.</p><ul>" + links + "</ul>").encode(), "text/html")
        if path == "/theme.css":
            try:
                return self.respond(theme_css().encode(), "text/css")
            except ValueError as error:
                return self.respond(str(error).encode(), "text/plain", 500)
        if not path.startswith("/fixtures/"):
            return self.respond(b"Not found", "text/plain", 404)
        file = (FIXTURES / path.removeprefix("/fixtures/")).resolve()
        if not file.is_relative_to(FIXTURES.resolve()) or not file.is_file():
            return self.respond(b"Not found", "text/plain", 404)
        data = file.read_bytes()
        if file.parent == FIXTURES and file.suffix == ".html" and parse_qs(route.query).get("theme") != ["original"]:
            data = data.replace(b"</head>", b'<link rel="stylesheet" id="current-theme" href="/theme.css"></head>', 1)
        content_type = mimetypes.guess_type(file.name)[0] or "application/octet-stream"
        return self.respond(data, content_type)

    def respond(self, body, content_type, status=200):
        self.send_response(status)
        self.send_header("Content-Type", content_type + ("; charset=utf-8" if content_type.startswith("text/") else ""))
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Security-Policy", CSP)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8914)
    args = parser.parse_args()
    theme_css()
    server = PreviewServer(("127.0.0.1", args.port), Handler)
    print(f"Preview: http://127.0.0.1:{args.port}/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
