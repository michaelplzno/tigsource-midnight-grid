"""Build offline, anonymized layout fixtures from explicitly supplied MHTML files.

Uses only Python's standard library. Original archives are never copied to the
fixture directory. Only the forum skin's CSS and interface images are retained.
"""

from __future__ import annotations

import argparse
from email import policy
from email.parser import BytesParser
from hashlib import sha256
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import struct
from urllib.parse import urljoin, urlsplit


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
VOID = set("area base br col embed hr img input link meta param source track wbr".split())
SKIP = {"script", "noscript", "object", "embed", "base", "style"}
SKIN_CSS = {"/Themes/tigsource/style.css", "/Themes/default/print.css"}
PUBLIC_SECTION_IDS = frozenset({"1", "2", "4", "8"})


def decode_text(part):
    # Chrome MHTML often omits a MIME charset despite the page being UTF-8.
    # EmailMessage.get_content() would default to ASCII and corrupt arrows,
    # accented titles, and other useful layout cases with replacement glyphs.
    text = (part.get_payload(decode=True) or b"").decode(part.get_content_charset() or "utf-8")
    return text.replace("\r\r\n", "\n").replace("\r\n", "\n").replace("\r", "\n")


class Node:
    def __init__(self, tag="", attrs=()):
        self.tag = tag
        self.attrs = dict(attrs)
        self.children: list[Node | str] = []

    def render(self):
        if not self.tag:
            return "".join(child.render() if isinstance(child, Node) else escape(child)
                           for child in self.children)
        attrs = "".join(" " + key + ("" if value is None else '="' + escape(value, quote=True) + '"')
                        for key, value in self.attrs.items())
        opening = "<" + self.tag + attrs + ">"
        if self.tag in VOID:
            return opening
        return opening + "".join(child.render() if isinstance(child, Node) else escape(child)
                                  for child in self.children) + "</" + self.tag + ">"


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def category_ids(node):
    return {anchor.attrs["name"] for heading in node.children
            if isinstance(heading, Node) and {"catbg", "catbg2"} & set((heading.attrs.get("class") or "").split())
            for anchor in heading.children
            if isinstance(anchor, Node) and anchor.tag == "a" and anchor.attrs.get("name")}


def dimensions(data):
    """Read common image dimensions without decoding images or adding packages."""
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    if data[:6] in (b"GIF87a", b"GIF89a") and len(data) >= 10:
        return struct.unpack("<HH", data[6:10])
    if data.startswith(b"\xff\xd8"):
        index = 2
        while index + 9 < len(data):
            if data[index] != 255:
                index += 1
                continue
            marker = data[index + 1]
            if marker in (0xD8, 0xD9):
                index += 2
                continue
            size = int.from_bytes(data[index + 2:index + 4], "big")
            if marker in (0xC0, 0xC1, 0xC2):
                height, width = struct.unpack(">HH", data[index + 5:index + 9])
                return width, height
            if size < 2:
                break
            index += size + 2
    return None


def synthetic_text(text):
    if not text.strip():
        return text
    # Keep the approximate wrapping pressure, whitespace, and original elements
    # while excluding copied post prose, signatures, email addresses, and URLs.
    sample = "Sample development update with a long description for layout testing. "
    def line(value):
        if not value.strip():
            return value
        leading = value[:len(value) - len(value.lstrip())]
        trailing = value[len(value.rstrip()):]
        size = len(value.strip())
        return leading + (sample * (size // len(sample) + 1))[:size] + trailing
    return "\n".join(line(value) for value in text.split("\n"))


class Builder:
    def __init__(self, archive, output):
        message = BytesParser(policy=policy.default).parsebytes(archive.read_bytes())
        parts = list(message.walk())
        main = next(part for part in parts
                    if part.get_content_type() == "text/html"
                    and urlsplit(str(part.get("Content-Location", ""))).hostname == "forums.tigsource.com")
        self.url = str(main["Content-Location"])
        self.document = Document(decode_text(main))
        self.parts = {str(part.get("Content-Location")): part for part in parts
                      if part.get("Content-Location")}
        self.output = output
        self.names = {}

    def write(self, relative, data):
        destination = self.output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, str):
            destination.write_text(data, encoding="utf-8", newline="\n")
        else:
            destination.write_bytes(data)
        return "/fixtures/" + relative

    def resource(self, location, base):
        absolute = urljoin(base, location)
        parsed = urlsplit(absolute)
        part = self.parts.get(absolute)
        path = parsed.path
        if (parsed.hostname == "forums.tigsource.com"
                and path.startswith(("/Themes/tigsource/images/", "/Themes/default/images/"))
                and ".." not in path.split("/") and part
                and part.get_content_type().startswith("image/")):
            return self.write("assets/legacy" + path, part.get_payload(decode=True))
        return None

    def css(self, location):
        part = self.parts.get(location)
        if not part or urlsplit(location).path not in SKIN_CSS:
            return None
        css = decode_text(part).replace("\r\n", "\n").replace("\r", "\n")
        def replace(match):
            value = match.group(1).strip().strip("\"'")
            target = self.resource(value, location)
            return 'url("' + target + '")' if target else "none"
        css = re.sub(r"url\(([^)]+)\)", replace, css, flags=re.I)
        css = re.sub(r"@charset\s+[^;]+;", "", css, flags=re.I).strip() + "\n"
        return self.write("assets/legacy" + urlsplit(location).path, css)

    def placeholder(self, location, avatar=False):
        part = self.parts.get(location)
        size = dimensions(part.get_payload(decode=True) or b"") if part else None
        width, height = size or ((64, 64) if avatar else (640, 360))
        width, height = max(1, min(width, 8192)), max(1, min(height, 8192))
        label = "Avatar" if avatar else "Sample post image"
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
               f'viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="#35495c"/>'
               f'<text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" '
               f'fill="#dce6ee" font-family="sans-serif" font-size="{min(24, height / 5)}">'
               f'{label}</text></svg>\n')
        # Never encode an original user's URL or filename in a public asset path.
        return self.write("assets/placeholders/" + sha256(location.encode()).hexdigest()[:16] + ".svg", svg)

    def clean(self, node, authored=False, account=False):
        if node.tag in SKIP or node.tag.startswith(("grammarly", "editorbx", "plasmo")):
            return None
        attrs = node.attrs
        classes = set((attrs.get("class") or "").split())
        authored = authored or bool(classes & {"post", "signature", "personalmessage"})
        account = account or "userinfo" in classes
        # Export only the allowlisted public forum sections, before copying assets.
        identifiers = category_ids(node) if "tborder" in classes else set()
        if identifiers and not identifiers <= PUBLIC_SECTION_IDS:
            return None
        if node.tag == "meta" and attrs.get("http-equiv", "").lower() != "content-type":
            return None
        if node.tag == "link":
            if attrs.get("rel", "").lower() != "stylesheet":
                return None
            target = self.css(attrs.get("href", ""))
            if not target:
                return None
            node.attrs = {"rel": "stylesheet", "href": target}
            if attrs.get("media"):
                node.attrs["media"] = attrs["media"]
            return node
        if node.tag == "input" and (attrs.get("type", "").lower() == "hidden"
                                   or re.fullmatch(r"[0-9a-f]{16,}", attrs.get("name", ""), re.I)):
            return None
        original_link = attrs.get("href", "")
        if node.tag == "a" and re.search(r"action=profile(?:[;&]|$)", original_link) and re.search(r"[;&]u=\d+", original_link):
            member = re.search(r"[;&]u=(\d+)", original_link)
            key = member.group(1) if member else "unknown"
            if key not in self.names:
                self.names[key] = "Fixture member " + str(len(self.names) + 1)
            if not any(isinstance(child, Node) and child.tag == "img" for child in node.children):
                node.children = [self.names[key]]
        if node.tag == "iframe":
            node.attrs = {key: value for key, value in attrs.items() if key in {"width", "height", "class", "style"}}
            node.attrs.update(src="/fixtures/assets/embed.html", title="Offline video placeholder")
            node.children = []
            return node
        cleaned = {}
        for key, value in attrs.items():
            if key.startswith("on") or key.startswith("data-") or key in {
                "title", "srcset", "ping", "integrity", "nonce", "crossorigin", "target",
                "formaction", "srcdoc", "poster", "background", "manifest", "contenteditable",
            }:
                continue
            if key in {"href", "action"}:
                value = "#fixture-link" if key == "href" else "#"
            elif key == "src":
                location = urljoin(self.url, value or "")
                avatar = bool(classes & {"avatar", "avatar_t"})
                value = self.resource(value or "", self.url) or self.placeholder(location, avatar)
            elif key == "style":
                value = re.sub(r"url\([^)]*\)", "none", value, flags=re.I)
            elif key == "value" and node.tag in {"input", "textarea"}:
                if attrs.get("type", "text").lower() not in {"submit", "button", "reset"}:
                    value = ""
            if value and (re.search(r"sesc=|PHPSESSID|session_id|session_var", value, re.I)
                          or re.fullmatch(r"[a-f0-9]{24,}", value, re.I)):
                continue
            cleaned[key] = value
        node.attrs = cleaned
        children = []
        for child in node.children:
            if isinstance(child, Node):
                result = self.clean(child, authored, account)
                if result is not None:
                    children.append(result)
            else:
                if authored:
                    child = synthetic_text(child)
                elif account and child.strip():
                    if node.tag == "h3":
                        child = "Hello "
                    elif node.tag == "b":
                        child = "FixtureUser"
                    elif node.tag == "a":
                        child = "3 messages" if "action=pm" in original_link else child
                    elif "Total time logged in" in child:
                        child = "Total time logged in: 1 day, 2 hours and 3 minutes."
                    elif "are new" in child:
                        child = " 0 are new."
                    elif "you have" in child:
                        child = "You have "
                    else:
                        child = synthetic_text(child)
                else:
                    child = re.sub(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "Logged", child)
                    child = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "fixture@example.invalid", child)
                    child = child.replace("michaelplzno", "FixtureUser")
                children.append(child)
        node.children = children
        return node

    def build(self, name):
        root = self.clean(self.document.root)
        text = "<!doctype html>\n" + root.render() + "\n"
        text = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
        # A redundant safeguard: the original snapshots contain neither private
        # form actions nor extension-injected frozen theme styles after cleaning.
        if re.search(r"sesc=|PHPSESSID|session_id|session_var|cid:|--tig-bg", text, re.I):
            raise ValueError("Unexpected session or frozen-style data in " + name)
        self.write(name + ".html", text)
        return {"page": name + ".html", "source": self.url.split(";sesc=")[0], "anonymized": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--board", type=Path, required=True)
    parser.add_argument("--topic", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=FIXTURES)
    args = parser.parse_args()
    pages = [Builder(path, args.output).build(name)
             for name, path in [("index", args.index), ("board", args.board), ("topic", args.topic)]]
    (args.output / "manifest.json").write_text(json.dumps({
        "description": "Anonymized SMF markup from author-supplied MHTML captures; current theme loaded separately.",
        "pages": pages,
    }, indent=2) + "\n", encoding="utf-8", newline="\n")
    (args.output / "assets" / "embed.html").write_text(
        '<!doctype html><meta charset="utf-8"><title>Offline video</title>'
        '<body style="margin:0;background:#35495c;color:#dce6ee;font:16px sans-serif;'
        'display:grid;place-items:center;min-height:100vh">Embedded video placeholder</body>\n',
        encoding="utf-8", newline="\n")
    print("Built:", ", ".join(page["page"] for page in pages))


if __name__ == "__main__":
    main()
