#!/usr/bin/env python3
"""Simple PDF extraction test using PyMuPDF."""

import os

import pymupdf


def main():
    pdf_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'documents', 'test.pdf')
    pdf_path = os.path.normpath(pdf_path)

    if not os.path.exists(pdf_path):
        print(f"PDF not found: {pdf_path}")
        return

    doc = pymupdf.open(pdf_path)
    page_count = doc.page_count
    print(f"Pages: {page_count}")

    if page_count > 0:
        page = doc[0]
        text = page.get_text()
        print("First page text (first 1000 chars):")
        print(text[:1000])
    else:
        print("PDF has no pages.")

    doc.close()


if __name__ == "__main__":
    main()
