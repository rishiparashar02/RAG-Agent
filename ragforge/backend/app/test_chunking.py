#!/usr/bin/env python3
"""Simple chunking test using PyMuPDF + LangChain RecursiveCharacterTextSplitter.

Reads first 2 pages of data/documents/test.pdf, splits each page's text into
chunks using `chunk_size=500`, `chunk_overlap=50`, and preserves metadata
(`source`, `page`). Prints total chunks, first 3 chunks, and their metadata.
"""

import os
from pprint import pprint
from typing import List, Dict

import pymupdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def read_first_n_pages(pdf_path: str, n: int = 2) -> List[Document]:
    if not os.path.exists(pdf_path):
        print(f"PDF not found: {pdf_path}")
        return []

    doc = pymupdf.open(pdf_path)
    documents: List[Document] = []
    try:
        total = min(n, doc.page_count)
        for i in range(total):
            page = doc[i]
            text = page.get_text()
            documents.append(
                Document(page_content=text, metadata={
                    "source": os.path.basename(pdf_path),
                    "page": i + 1,
                })
            )
    finally:
        doc.close()

    return documents


def chunk_pages(documents: List[Document], chunk_size: int = 500, chunk_overlap: int = 50) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    # split_documents returns list[Document]
    chunks = splitter.split_documents(documents)
    return chunks


def main():
    pdf_path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "..", "data", "documents", "test.pdf")
    )

    documents = read_first_n_pages(pdf_path, n=2)
    if not documents:
        return

    chunks = chunk_pages(documents, chunk_size=500, chunk_overlap=50)

    print(f"Total chunks: {len(chunks)}")
    print("First 3 chunks and metadata:")
    for c in chunks[:3]:
        print("--- chunk ---")
        print("content:")
        print(c.page_content[:500])
        print("metadata:")
        pprint(c.metadata)


if __name__ == "__main__":
    main()
