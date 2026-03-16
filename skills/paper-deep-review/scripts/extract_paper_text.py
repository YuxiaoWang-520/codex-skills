#!/usr/bin/env python3
"""
Extract text from a PDF paper and generate:
- full_text.txt
- pages/page_XXX.txt
- section_index.json (heuristic)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Tuple


ROMAN_SECTION_RE = re.compile(r"^\s*(?:[IVXLC]+\.)\s*(.+?)\s*$")
INLINE_ROMAN_RE = re.compile(r"(?:^|\s)([IVXLC]+\.)\s*([A-Z][A-Z0-9\s\-:&/]{2,})")
PLAIN_SECTION_RE = re.compile(
    r"^\s*(?:\d+\.?\s+)?(INTRODUCTION|MOTIVATION|PRELIMINARIES|METHOD|METHODS|APPROACH|"
    r"EXPERIMENT|EVALUATION|RELATED WORK|CONCLUSION|ABSTRACT)\s*$",
    re.IGNORECASE,
)


def _extract_with_pdfplumber(pdf_path: Path) -> List[str]:
    import pdfplumber  # type: ignore

    pages: List[str] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return pages


def _extract_with_pypdf(pdf_path: Path) -> List[str]:
    from pypdf import PdfReader  # type: ignore

    pages: List[str] = []
    reader = PdfReader(str(pdf_path))
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return pages


def extract_pages(pdf_path: Path) -> Tuple[str, List[str]]:
    errors = []

    try:
        return "pdfplumber", _extract_with_pdfplumber(pdf_path)
    except Exception as exc:  # pragma: no cover
        errors.append(f"pdfplumber failed: {exc}")

    try:
        return "pypdf", _extract_with_pypdf(pdf_path)
    except Exception as exc:  # pragma: no cover
        errors.append(f"pypdf failed: {exc}")

    err = "\n".join(errors) if errors else "No extractor available"
    raise RuntimeError(
        "Failed to extract PDF text. Install pdfplumber or pypdf.\n" + err
    )


def build_section_index(full_text: str) -> List[dict]:
    sections: List[dict] = []
    lines = full_text.splitlines()
    seen = set()

    def _accept_heading(title_raw: str) -> bool:
        alpha = re.sub(r"[^A-Za-z ]", "", title_raw).strip()
        if len(alpha) < 3:
            return False
        alpha_chars = re.sub(r"[^A-Za-z]", "", alpha)
        if not alpha_chars:
            return False
        upper_ratio = sum(1 for c in alpha_chars if c.isupper()) / len(alpha_chars)
        return upper_ratio >= 0.6

    for idx, raw in enumerate(lines, start=1):
        line = raw.replace("\x00", "").strip()
        if not line:
            continue

        m1 = ROMAN_SECTION_RE.match(line)
        if m1:
            title_raw = m1.group(1).strip()
            if not _accept_heading(title_raw):
                continue
            key = (idx, title_raw)
            if key in seen:
                continue
            seen.add(key)
            sections.append(
                {
                    "line": idx,
                    "type": "roman",
                    "title": title_raw,
                    "raw": line,
                }
            )
            continue

        for m_inline in INLINE_ROMAN_RE.finditer(line):
            roman = m_inline.group(1).strip()
            title_raw = m_inline.group(2).strip()
            if not _accept_heading(title_raw):
                continue
            key = (idx, f"{roman} {title_raw}")
            if key in seen:
                continue
            seen.add(key)
            sections.append(
                {
                    "line": idx,
                    "type": "roman-inline",
                    "title": title_raw,
                    "raw": f"{roman} {title_raw}",
                }
            )

        m2 = PLAIN_SECTION_RE.match(line)
        if m2:
            sections.append(
                {
                    "line": idx,
                    "type": "plain",
                    "title": m2.group(1).strip(),
                    "raw": line,
                }
            )

    return sections


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract text and sections from PDF")
    parser.add_argument("pdf", type=Path, help="Input PDF path")
    parser.add_argument("--outdir", type=Path, required=True, help="Output directory")
    args = parser.parse_args()

    pdf_path = args.pdf.expanduser().resolve()
    outdir = args.outdir.expanduser().resolve()

    if not pdf_path.exists():
        print(f"Input PDF not found: {pdf_path}", file=sys.stderr)
        return 1

    pages_dir = outdir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    engine, pages = extract_pages(pdf_path)

    cleaned_pages: List[str] = []
    for i, page_text in enumerate(pages, start=1):
        text = (page_text or "").replace("\x00", "")
        cleaned_pages.append(text)
        (pages_dir / f"page_{i:03d}.txt").write_text(text, encoding="utf-8")

    full_text = "\n\n".join(
        [f"===== PAGE {i} =====\n{t}" for i, t in enumerate(cleaned_pages, start=1)]
    )

    (outdir / "full_text.txt").write_text(full_text, encoding="utf-8")

    section_index = build_section_index(full_text)
    (outdir / "section_index.json").write_text(
        json.dumps(
            {
                "pdf": str(pdf_path),
                "engine": engine,
                "page_count": len(cleaned_pages),
                "sections": section_index,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(json.dumps({"engine": engine, "pages": len(cleaned_pages), "outdir": str(outdir)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
