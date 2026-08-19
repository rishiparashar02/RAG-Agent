#!/usr/bin/env python3
"""Reusable retrieval function for RAG pipeline."""

import os

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


def retrieve_documents(question: str, k: int = 3):
    """Retrieve documents from ChromaDB using semantic similarity.
    
    Args:
        question: Query text to search for
        k: Number of documents to retrieve (default 3)
        
    Returns:
        List of LangChain Document objects with metadata (source, page)
    """
    persist_dir = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "..", "data", "chroma")
    )
    embeddings = OllamaEmbeddings(model="qwen3-embedding:0.6b")
    vector_store = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings,
        collection_name="ragforge_test_docs",
    )
    
    docs = vector_store.similarity_search(question, k=k)
    return docs
