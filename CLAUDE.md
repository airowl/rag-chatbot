# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

RAG chatbot: upload PDFs, ask questions answered from their content. Python/FastAPI backend (`app/`) + Vue 3/TypeScript SPA (`frontend/`). Retrieval via ChromaDB, embeddings + LLM both via a locally-running Ollama `mistral` model.

For an extended architecture write-up (design patterns, modification points, deployment notes), see `.github/copilot-instructions.md`. This file stays focused on commands and non-obvious constraints.

## Commands

### Backend
```bash
# Ollama must run on the HOST first (not in Docker):
ollama serve
ollama pull mistral

# Full stack (backend :8000, frontend :5173):
docker-compose up

# Backend alone, locally (from repo root, so `app.main` resolves):
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev          # Vite dev server, hot reload
npm run build        # runs type-check (vue-tsc) THEN vite build — build fails on type errors
npm run type-check   # vue-tsc --build, no emit
```

No test suite exists in either backend or frontend — there is nothing to run for tests yet.

## Architecture

Three backend modules form a linear RAG flow:

- `app/main.py` — FastAPI app + CORS. Two endpoints, **no trailing slash**:
  - `POST /upload` (multipart `file`) → writes to `data/docs/{filename}` → calls `create_vector_store()` synchronously (request blocks until embeddings finish).
  - `GET /ask?query=...` → returns `{answer}`.
- `app/embeddings.py` — `create_vector_store(pdf_path)` loads the PDF with `PyPDFLoader` and adds it to the persisted Chroma DB at `chroma/`. `load_vector_store()` reopens that same DB.
- `app/rag_pipeline.py` — `build_rag_pipeline()` builds a LangChain `RetrievalQA` chain from the vector store.

Frontend is a single `App.vue` (Composition API, Italian UI text). `frontend/src/api.ts` hardcodes `baseURL: http://localhost:8000`. The router (`frontend/src/router/index.ts`) has an empty `routes: []` — the app is one component, routing is unused.

## Non-obvious constraints

- **`build_rag_pipeline()` runs on every `/ask`** — it reloads the vector store and re-instantiates the LLM per request; there is no caching.
- **Single shared vector space, no document isolation.** Every uploaded PDF lands in the same `chroma/` collection, so every query searches across all documents. Per-document filtering would need metadata or separate collections.
- **`mistral` is used for BOTH embeddings (`OllamaEmbeddings`) and generation (`OllamaLLM`).** Changing the model means re-pulling it and rebuilding `chroma/` (embedding dimensions must match existing vectors).
- **Ollama is reached over the host.** Docker backend uses `OLLAMA_HOST=host.docker.internal:11434` + `extra_hosts: host.docker.internal:host-gateway`. Ollama itself is never containerized here.
- **`chromadb` is pinned to `==0.4.13`** in `requirements.txt` (intentional, per recent versioning fix). Other deps are floors (`>=`). Be cautious bumping chromadb.
- **`data/docs/` and `chroma/` are gitignored and Docker volume-mounted.** `POST /upload` writes directly into `data/docs/` — that directory must exist or the write fails. Both are persistence dirs, not source.
- Upload does no filename sanitization/validation; CORS is fully open (`allow_origins=["*"]`); endpoints have no auth. Dev-only posture.
