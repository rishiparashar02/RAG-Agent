from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="RAGForge Backend")

origins = os.getenv("CORS_ORIGINS", "*")
if origins == "*":
    allow_origins = ["*"]
else:
    allow_origins = [o.strip() for o in origins.split(',')]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}
