#!/usr/bin/env python3
"""Reusable LLM answer generation for RAG pipeline."""

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


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


def generate_answer(question, documents):
    llm = ChatOllama(model="qwen3:4b")
    prompt = build_prompt(question, documents)
    result = llm.invoke(prompt.format_messages())
    return result.content
