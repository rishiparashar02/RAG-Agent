from langchain_ollama import ChatOllama


llm = ChatOllama(model="qwen3:4b")

response = llm.invoke("Explain RAG in one sentence.")

print(response)
