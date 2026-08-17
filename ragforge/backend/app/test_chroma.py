#!/usr/bin/env python3
"""Minimal ChromaDB test using OllamaEmbeddings."""

import chromadb

try:
    from langchain.embeddings import OllamaEmbeddings
except ImportError:
    from langchain_ollama import OllamaEmbeddings


def main():
    client = chromadb.Client()
    collection = client.create_collection(name="ragforge_chroma_test")

    docs = [
        "Python is a programming language commonly used for data science and machine learning.",
        "React is a JavaScript library used for building user interfaces.",
        "FastAPI is a Python framework for building APIs.",
    ]

    metadatas = [
        {"source": "doc1", "topic": "python"},
        {"source": "doc2", "topic": "react"},
        {"source": "doc3", "topic": "fastapi"},
    ]

    embeddings = OllamaEmbeddings(model="qwen3-embedding:0.6b")
    document_embeddings = embeddings.embed_documents(docs)

    collection.add(
        ids=["python-doc", "react-doc", "fastapi-doc"],
        documents=docs,
        metadatas=metadatas,
        embeddings=document_embeddings,
    )

    query = "Which technology is used to build APIs with Python?"
    query_embedding = embeddings.embed_query(query)

    results = collection.query(query_embeddings=[query_embedding], n_results=1)
    retrieved_doc = results["documents"][0][0]
    retrieved_metadata = results["metadatas"][0][0]

    print("Retrieved document:", retrieved_doc)
    print("Metadata:", retrieved_metadata)


if __name__ == "__main__":
    main()
