#!/usr/bin/env python3
"""Simple PDF ingestion smoke test into ChromaDB.

Loads all pages from data/documents/test.pdf, splits pages into chunks, embeds
chunks with OllamaEmbeddings, stores them in a local ChromaDB collection under
`data/chroma`, and runs a similarity search for a sample prompt.
"""

import os
from pprint import pprint

import pymupdf
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def read_all_pages(pdf_path: str):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = pymupdf.open(pdf_path)
    documents = []
    try:
        for page_number in range(doc.page_count):
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

    documents = read_all_pages(pdf_path)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.split_documents(documents)

    persist_dir = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "..", "data", "chroma")
    )
    os.makedirs(persist_dir, exist_ok=True)

    embeddings = OllamaEmbeddings(model="qwen3-embedding:0.6b")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir,
        collection_name="ragforge_test_docs",
    )
    vector_store.persist()

    query = "How does dust affect solar panel efficiency?"
    results = vector_store.similarity_search(query, k=3)

    print(f"Number of chunks: {len(chunks)}")
    print(f"Top 3 retrieved chunks for: {query}")
    for item in results:
        print("---")
        print(item.page_content[:500])
        pprint(item.metadata)


if __name__ == "__main__":
    main()
