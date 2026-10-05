#!/usr/bin/env python3
"""Simple local RAG CLI test using Chroma + Ollama.

Loads the existing local ChromaDB at data/chroma, performs a similarity search,
constructs a prompt from retrieved context, and asks the local ChatOllama model
for a concise answer grounded only in the provided documents.
"""

from rag.rag_service import ask_question
from rag.rag_service import last_generation_latency_s
from rag.rag_service import last_retrieval_latency_ms
from rag.rag_service import last_total_latency_s


def main():
    question = input("Ask a question: ").strip()
    if not question:
        print("Question cannot be empty.")
        return

    answer, docs = ask_question(question, k=3)
    retrieval_latency_ms = last_retrieval_latency_ms
    generation_latency_s = last_generation_latency_s
    total_latency_s = last_total_latency_s

    print("\nQuestion:")
    print(question)
    print("\nAnswer:")
    print(answer)

    pages = sorted({doc.metadata.get("page") for doc in docs if doc.metadata.get("page") is not None})
    print("\nRetrieved source pages:")
    print(pages)

    print("\n" + "="*40)
    print("RAG PERFORMANCE")
    print("="*40)
    print(f"Retrieved chunks: {len(docs)}")
    print(f"Retrieval latency: {retrieval_latency_ms:.2f} ms")
    print(f"LLM generation latency: {generation_latency_s:.2f} s")
    print(f"Total RAG latency: {total_latency_s:.2f} s")
    print("="*40)


if __name__ == "__main__":
    main()
