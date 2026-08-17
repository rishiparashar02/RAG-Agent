# RAGForge — Project Foundation

This repository contains foundation scaffold for RAGForge (local-first RAG app).

Structure:

- backend: FastAPI backend
- frontend: React + Vite frontend
- data/documents: storage for uploaded documents

Quickstart

Backend

1. Create virtualenv and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r backend/requirements.txt
```

2. Run backend:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend

1. Install dependencies and run dev server:

```bash
cd frontend
npm install
npm run dev
```

Verify

- Backend health: `http://localhost:8000/health`
- Frontend: open `http://localhost:5173` (Vite default)

Environment

- See `backend/.env.example` and `frontend/.env.example` for variables.

Notes

- Local-first. No paid APIs required.
- RAG pipeline, ingestion, embeddings, and agent will be added incrementally.
