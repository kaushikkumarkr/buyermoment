from __future__ import annotations

import csv
import io
import json
import re
import urllib.request
import zipfile
from html.parser import HTMLParser
from xml.etree import ElementTree

from .security import safe_filename, validate_upload_size


class _TextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self._skip = False

    def handle_starttag(self, tag: str, attrs) -> None:  # noqa: ANN001
        self._skip = tag.lower() in {"script", "style", "noscript"}

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style", "noscript"}:
            self._skip = False

    def handle_data(self, data: str) -> None:
        if not self._skip and data.strip():
            self.parts.append(data.strip())


def html_to_text(content: str) -> str:
    parser = _TextParser()
    parser.feed(content)
    return "\n".join(parser.parts)


def _docx_to_text(content: bytes) -> str:
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        xml = archive.read("word/document.xml")
    root = ElementTree.fromstring(xml)
    text = [node.text or "" for node in root.iter() if node.tag.endswith("}t")]
    return " ".join(text)


def parse_file(filename: str, content: bytes) -> tuple[str, str]:
    safe = safe_filename(filename)
    validate_upload_size(content)
    suffix = safe.rsplit(".", 1)[-1].lower()
    if suffix in {"txt", "md", "csv", "json", "html", "htm"}:
        raw = content.decode("utf-8-sig")
    elif suffix == "docx":
        raw = _docx_to_text(content)
    elif suffix == "pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise ValueError("PDF ingestion requires the optional pypdf dependency") from exc
        raw = "\n".join(page.extract_text() or "" for page in PdfReader(io.BytesIO(content)).pages)
    else:
        raise ValueError(f"unsupported file type: .{suffix}")
    if suffix in {"html", "htm"}:
        raw = html_to_text(raw)
    elif suffix == "csv":
        rows = csv.reader(io.StringIO(raw))
        raw = "\n".join(" | ".join(cell.strip() for cell in row) for row in rows)
    elif suffix == "json":
        raw = json.dumps(json.loads(raw), ensure_ascii=False, indent=2)
    normalized = re.sub(r"\n{3,}", "\n\n", raw).strip()
    if not normalized:
        raise ValueError("file contains no extractable text")
    return safe, normalized


def fetch_website(url: str, *, max_bytes: int = 2_000_000) -> tuple[str, str]:
    if not url.startswith(("https://", "http://")):
        raise ValueError("website URL must use http or https")
    request = urllib.request.Request(url, headers={"User-Agent": "BuyerMomentEvidenceBot/1.0"})
    with urllib.request.urlopen(request, timeout=15) as response:  # noqa: S310
        content = response.read(max_bytes + 1)
        content_type = response.headers.get_content_type()
    validate_upload_size(content[:max_bytes])
    if len(content) > max_bytes:
        raise ValueError("website response exceeds size limit")
    text = content.decode("utf-8", errors="replace")
    return content_type, html_to_text(text) if "html" in content_type else text
