#!/usr/bin/env python3
"""Extract per-page metadata from a PDF using PyMuPDF.

Simple script: read data/documents/test.pdf, produce per-page records:
- source: PDF filename
- page: 1-based page number
- text: full page text (no chunking)

Prints records for first 2 pages.
"""

import os
from pprint import pprint

import pymupdf


def extract_metadata(pdf_path: str):
    if not os.path.exists(pdf_path):
        print(f"PDF not found: {pdf_path}")
        return []

    doc = pymupdf.open(pdf_path)
    records = []
    try:
        for i in range(doc.page_count):
            page = doc[i]
            text = page.get_text()
            records.append({
                "source": os.path.basename(pdf_path),
                "page": i + 1,
                "text": text,
            })
    finally:
        doc.close()

    return records


def main():
    pdf_path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "..", "data", "documents", "test.pdf")
    )

    records = extract_metadata(pdf_path)
    if not records:
        return

    print("First 2 page records:")
    pprint(records[:2])


if __name__ == "__main__":
    main()
