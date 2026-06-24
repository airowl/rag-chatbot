# RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions based on the content of PDF files you upload. Embeddings and answer generation both run locally through an Ollama `mistral` model — no external API keys required.

## How it works

1. The user uploads a PDF.
2. The backend saves it to `data/docs/` and splits it into chunks.
3. Each chunk is converted into an embedding and stored in ChromaDB.
4. The user asks a question.
5. The backend embeds the question and retrieves the most similar chunks from ChromaDB.
6. The chunks and the question are combined into a prompt and sent to Ollama.
7. Ollama generates the answer, which the backend returns to the user.

## Tech stack

- **Python / FastAPI** — backend API
- **LangChain** — RAG orchestration (`RetrievalQA`)
- **ChromaDB** — vector store for embeddings (persisted to `chroma/`)
- **Ollama (`mistral`)** — embeddings and LLM inference
- **Vue 3 + TypeScript + Vite** — frontend UI
- **Docker / Docker Compose** — containerized backend and frontend

## Prerequisites

Ollama must be running on the host machine (it is **not** containerized by this project):

```bash
ollama serve
ollama pull mistral
```

## Running with Docker

```bash
docker-compose up
```

- Backend: http://localhost:8000
- Frontend: http://localhost:5173

The backend reaches Ollama on the host via `host.docker.internal:11434`. The `data/` and `chroma/` directories are volume-mounted, so uploaded PDFs and embeddings persist across restarts.

## Running locally (without Docker)

Backend (from the repository root, so `app.main` resolves):

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## API

| Method | Endpoint      | Description                                                        |
| ------ | ------------- | ----------------------------------------------------------------- |
| `POST` | `/upload`     | Upload a PDF (multipart `file`). Saves it and creates embeddings. |
| `GET`  | `/ask?query=` | Ask a question; returns `{ "answer": "..." }`.                    |

## Notes & limitations

- All uploaded PDFs share a single ChromaDB collection, so every question is answered against **all** documents at once — there is no per-document filtering.
- `mistral` is used for both embeddings and generation. Changing the model requires re-pulling it and rebuilding the `chroma/` directory.
- CORS is fully open and there is no authentication. This is a development setup, not production-ready.

## What I learned from this project

The basics of how an LLM can read and reason over uploaded data: how to handle file uploads, persist them, and convert their content into vectors. The core RAG concepts — embeddings, vector databases, prompt construction, and LLM processing to generate grounded answers.
