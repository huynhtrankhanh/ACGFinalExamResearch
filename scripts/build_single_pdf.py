#!/usr/bin/env python3
"""Build a single printable PDF from all study guides with robust word wrapping."""
from __future__ import annotations

from pathlib import Path
import datetime

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_MD = ROOT / "ACG_Final_Print_Packet.md"
OUTPUT_PDF = ROOT / "ACG_Final_Print_Packet.pdf"

SOURCE_FILES = [
    "ACG_Final_Exam_Study_Book.md",
    "advanced_exam_booster.md",
    "vr_ar.md",
    "delaunay_triangulation.md",
    "marching_cubes.md",
    "mri_ct_scanning.md",
    "brain_tumor_detection.md",
    "bezier_curves.md",
    "de_casteljau_algorithm.md",
    "bezier_surfaces.md",
    "bezier_surfaces_2.md",
]


def build_markdown() -> str:
    today = datetime.date.today().isoformat()
    parts = [
        "# ACG Final Exam Print Packet (Single Combined Edition)",
        "",
        f"Generated on: {today}",
        "",
        "This packet combines all repository study guides plus an advanced internet-researched booster section.",
        "",
        "## Included Documents",
    ]
    for name in SOURCE_FILES:
        parts.append(f"- {name}")
    parts.append("\n---\n")

    for name in SOURCE_FILES:
        path = ROOT / name
        if not path.exists():
            parts.append(f"\n# Missing File: {name}\n")
            continue
        parts.append(f"\n\n# Source: {name}\n")
        parts.append(path.read_text(encoding="utf-8"))
        parts.append("\n\n---\n")

    text = "\n".join(parts)
    OUTPUT_MD.write_text(text, encoding="utf-8")
    return text


def pdf_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def wrap_line(line: str, width: int) -> list[str]:
    if line == "":
        return [""]
    line = line.replace("\t", "    ")
    chunks: list[str] = []
    current = line
    while len(current) > width:
        # prefer wrapping on whitespace near boundary
        split = current.rfind(" ", 0, width + 1)
        if split <= 0:
            split = width
        chunks.append(current[:split])
        current = current[split:].lstrip()
    chunks.append(current)
    return chunks


def text_to_pages(text: str, max_chars: int = 95, lines_per_page: int = 64) -> list[list[str]]:
    all_lines: list[str] = []
    for raw in text.splitlines():
        all_lines.extend(wrap_line(raw, max_chars))

    pages: list[list[str]] = []
    i = 0
    while i < len(all_lines):
        pages.append(all_lines[i : i + lines_per_page])
        i += lines_per_page
    if not pages:
        pages = [["(empty)"]]
    return pages


def build_pdf_from_text(text: str) -> None:
    pages = text_to_pages(text)

    objects: list[bytes] = []

    # 1: Catalog, 2: Pages, 3: Font
    # Page objects and streams start at 4

    # Placeholder to append later with known child ids
    objects.append(b"")  # 1
    objects.append(b"")  # 2
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>")  # 3

    page_ids: list[int] = []
    stream_ids: list[int] = []

    for lines in pages:
        content_lines = [
            "BT",
            "/F1 9 Tf",
            "11 TL",
            "54 738 Td",
        ]
        for line in lines:
            content_lines.append(f"({pdf_escape(line)}) Tj")
            content_lines.append("T*")
        content_lines.append("ET")
        stream_text = "\n".join(content_lines).encode("latin-1", errors="replace")
        stream_obj = (
            f"<< /Length {len(stream_text)} >>\nstream\n".encode("ascii")
            + stream_text
            + b"\nendstream"
        )
        objects.append(stream_obj)
        stream_id = len(objects)
        stream_ids.append(stream_id)

        page_obj = f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 3 0 R >> >> /Contents {stream_id} 0 R >>".encode(
            "ascii"
        )
        objects.append(page_obj)
        page_id = len(objects)
        page_ids.append(page_id)

    kids = " ".join(f"{pid} 0 R" for pid in page_ids)
    objects[1] = f"<< /Type /Pages /Count {len(page_ids)} /Kids [ {kids} ] >>".encode("ascii")
    objects[0] = b"<< /Type /Catalog /Pages 2 0 R >>"

    pdf = bytearray()
    pdf.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{i} 0 obj\n".encode("ascii"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {len(objects)+1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        pdf.extend(f"{off:010d} 00000 n \n".encode("ascii"))

    pdf.extend(
        (
            f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF\n"
        ).encode("ascii")
    )

    OUTPUT_PDF.write_bytes(pdf)


def main() -> None:
    text = build_markdown()
    build_pdf_from_text(text)
    print(f"Wrote: {OUTPUT_MD}")
    print(f"Wrote: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
