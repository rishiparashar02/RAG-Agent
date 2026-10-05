#!/usr/bin/env python3
"""Service layer to orchestrate retrieval and answer generation."""

import time

from llm.generator import generate_answer
from retrieval.retriever import retrieve_documents


last_retrieval_latency_ms = 0.0
last_generation_latency_s = 0.0
last_total_latency_s = 0.0


def ask_question(question, k=3):
    global last_retrieval_latency_ms, last_generation_latency_s, last_total_latency_s

    total_start = time.perf_counter()

    retrieval_start = time.perf_counter()
    docs = retrieve_documents(question, k=k)
    retrieval_end = time.perf_counter()
    last_retrieval_latency_ms = (retrieval_end - retrieval_start) * 1000

    generation_start = time.perf_counter()
    answer = generate_answer(question, docs)
    generation_end = time.perf_counter()
    last_generation_latency_s = generation_end - generation_start

    last_total_latency_s = time.perf_counter() - total_start
    return answer, docs
