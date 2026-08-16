#!/usr/bin/env python3
"""Simple local RAG CLI test using Chroma + Ollama.

Loads the existing local ChromaDB at data/chroma, performs a similarity search,
constructs a prompt from retrieved context, and asks the local ChatOllama model
for a concise answer grounded only in the provided documents.
"""

import os

from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama, OllamaEmbeddings


def build_prompt(question: str, docs):
    context_blocks = []
    for doc in docs:
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "unknown")
        text = doc.page_content.strip()
        context_blocks.append(
            f"Source: {source}\nPage: {page}\nContext:\n{text}\n"
        )

    context_text = "\n\n---\n\n".join(context_blocks)

    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Answer using ONLY the provided context. If the answer cannot be found in the context, say that the information is not available in the provided documents. Do not invent facts. Give a concise answer. At the end, list the source pages used.",
            ),
            ("human", f"Context:\n{context_text}\n\nQuestion: {question}"),
        ]
    )


def main():
    persist_dir = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "..", "data", "chroma")
    )
    embeddings = OllamaEmbeddings(model="qwen3-embedding:0.6b")
    vector_store = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings,
        collection_name="ragforge_test_docs",
    )

    question = input("Ask a question: ").strip()
    if not question:
        print("Question cannot be empty.")
        return

    docs = vector_store.similarity_search(question, k=3)
    llm = ChatOllama(model="qwen3:4b")
    prompt = build_prompt(question, docs)
    result = llm.invoke(prompt.format_messages())

    print("\nQuestion:")
    print(question)
    print("\nAnswer:")
    print(result.content)

    pages = sorted({doc.metadata.get("page") for doc in docs if doc.metadata.get("page") is not None})
    print("\nRetrieved source pages:")
    print(pages)


if __name__ == "__main__":
    main()
