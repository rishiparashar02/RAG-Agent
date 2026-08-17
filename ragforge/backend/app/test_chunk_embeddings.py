#!/usr/bin/env python3
"""Simple PDF chunk embedding smoke test.

Reads the first 2 pages of data/documents/test.pdf, splits each page into
chunks, embeds the chunks with OllamaEmbeddings, and prints the first chunk's
embedding summary.
"""

import os
from pprint import pprint

import pymupdf
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def read_first_pages(pdf_path: str, page_limit: int = 2):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = pymupdf.open(pdf_path)
    documents = []
    try:
        total_pages = min(page_limit, doc.page_count)
        for page_number in range(total_pages):
            page = doc[page_number]
            text = page.get_text()
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": "test.pdf",
                        "page": page_number + 1,
                    },
                )
            )
    finally:
        doc.close()

    return documents


def main():
    pdf_path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "..", "data", "documents", "test.pdf")
    )

    documents = read_first_pages(pdf_path, page_limit=2)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.split_documents(documents)

    embeddings = OllamaEmbeddings(model="qwen3-embedding:0.6b")
    vector = embeddings.embed_query(chunks[0].page_content)

    print(f"Number of chunks: {len(chunks)}")
    print(f"Embedding vector dimension: {len(vector)}")
    print(f"First 5 values of the first embedding: {vector[:5]}")
    print("Metadata of the first chunk:")
    pprint(chunks[0].metadata)


if __name__ == "__main__":
    main()
