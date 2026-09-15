"""Load mixed knowledge files into a common document shape."""

from __future__ import annotations

import csv
import html
import json
import re
from html.parser import HTMLParser
from io import StringIO
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from lib.paths import DATA, ROOT

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,4})\s+(.*)$", re.MULTILINE)

SKIP_NAMES = {"readme.md", "manifest.yaml"}
TEXT_TYPES = {".md", ".txt", ".tsx", ".ts", ".jsx", ".js", ".html", ".htm", ".json", ".yaml", ".yml", ".csv", ".tsv", ".pdf"}


class Document(BaseModel):
    doc_id: str
    title: str
    text: str
    source_path: str
    source_type: str
    classification: str = "internal"
    status: str = "current"
    effective_date: str = "1970-01-01"
    department: str = "general"
    audience: str = "employee"
    rows: list[dict] = Field(default_factory=list)


class _HTMLText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self._skip = True
        if tag in {"p", "div", "br", "li", "h1", "h2", "h3", "h4", "tr"}:
            self.parts.append("\n")
        if tag in {"h1", "h2", "h3", "h4"}:
            level = tag[1]
            self.parts.append(f"{'#' * int(level)} ")

    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            self._skip = False
        if tag in {"p", "div", "li", "h1", "h2", "h3", "h4"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)

    def text(self) -> str:
        raw = html.unescape("".join(self.parts))
        return re.sub(r"\n{3,}", "\n\n", raw).strip() + "\n"


def load_manifest(folder: Path | None = None) -> dict[str, dict]:
    folder = folder or DATA
    path = folder / "manifest.yaml"
    if not path.exists():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out = {}
    for item in payload.get("documents") or []:
        rel = str(item["path"]).replace("\\", "/")
        out[rel] = item
    return out


def list_source_files(folder: Path | None = None) -> list[Path]:
    folder = folder or DATA
    files = []
    for path in sorted(folder.rglob("*")):
        if not path.is_file():
            continue
        if path.name.lower() in SKIP_NAMES:
            continue
        if path.suffix.lower() not in TEXT_TYPES:
            continue
        files.append(path)
    return files


def _rel(path: Path, folder: Path) -> str:
    try:
        return path.relative_to(folder).as_posix()
    except ValueError:
        return path.relative_to(ROOT).as_posix()


def _pdf_text(path: Path) -> str:
    from pypdf import PdfReader

    pages = []
    for page in PdfReader(str(path)).pages:
        pages.append(page.extract_text() or "")
    return "\n\n".join(pages).strip() + "\n"


def _csv_rows(path: Path) -> tuple[str, list[dict]]:
    raw = path.read_text(encoding="utf-8")
    dialect = csv.excel_tab if path.suffix.lower() == ".tsv" else csv.excel
    reader = csv.DictReader(StringIO(raw), dialect=dialect)
    rows = [dict(row) for row in reader]
    header = ", ".join(reader.fieldnames or [])
    lines = [f"Columns: {header}"]
    for row in rows:
        lines.append(" | ".join(f"{k}={v}" for k, v in row.items()))
    return "\n".join(lines) + "\n", rows


def _html_text(path: Path) -> str:
    parser = _HTMLText()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.text()


def _json_text(path: Path) -> str:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return json.dumps(payload, indent=2) + "\n"


def _yaml_text(path: Path) -> str:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return yaml.safe_dump(payload, sort_keys=False)


def _md_parts(raw: str) -> tuple[dict, str]:
    match = FRONTMATTER_RE.match(raw if raw.endswith("\n") else raw + "\n")
    if not match:
        return {}, raw
    meta = yaml.safe_load(match.group(1)) or {}
    return meta, match.group(2).strip() + "\n"


def _read_file(path: Path) -> tuple[str, list[dict]]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return _pdf_text(path), []
    if suffix in {".csv", ".tsv"}:
        return _csv_rows(path)
    if suffix in {".html", ".htm"}:
        return _html_text(path), []
    if suffix == ".json":
        return _json_text(path), []
    if suffix in {".yaml", ".yml"}:
        return _yaml_text(path), []
    raw = path.read_text(encoding="utf-8")
    if suffix == ".md":
        _meta, body = _md_parts(raw)
        return body, []
    return raw, []


def load_documents(folder: Path | None = None) -> list[Document]:
    folder = folder or DATA
    catalog = load_manifest(folder)
    docs: list[Document] = []
    for path in list_source_files(folder):
        rel = _rel(path, folder)
        listed = catalog.get(rel, {})
        text, rows = _read_file(path)
        extra, body = ({}, text)
        if path.suffix.lower() == ".md":
            extra, body = _md_parts(path.read_text(encoding="utf-8"))
            if extra:
                text = body
        meta = {**extra, **listed}
        for key in ("effective_date", "version", "doc_id", "title", "status"):
            if key in meta and meta[key] is not None:
                meta[key] = str(meta[key])
        docs.append(
            Document(
                doc_id=str(meta.get("doc_id") or path.stem),
                title=str(meta.get("title") or path.stem),
                text=text,
                source_path=rel,
                source_type=path.suffix.lower().lstrip("."),
                classification=str(meta.get("classification") or "internal"),
                status=str(meta.get("status") or "current"),
                effective_date=str(meta.get("effective_date") or "1970-01-01"),
                department=str(meta.get("department") or "general"),
                audience=str(meta.get("audience") or "employee"),
                rows=rows,
            )
        )
    return docs


def sections(body: str) -> list[tuple[str, str]]:
    matches = list(HEADING_RE.finditer(body))
    if not matches:
        return [("Overview", body.strip())]
    out = []
    preamble = body[: matches[0].start()].strip()
    if preamble:
        out.append(("Preamble", preamble))
    for i, match in enumerate(matches):
        title = match.group(2).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        text = body[start:end].strip()
        if text:
            out.append((title, text))
    return out
