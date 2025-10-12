# RAG Chatbot Project - AI Coding Agent Instructions

## Architecture Overview

This is a **Retrieval-Augmented Generation (RAG) chatbot** with a clean separation between:
- **Backend**: Python FastAPI service (`app/`) using LangChain + Ollama + Chroma
- **Frontend**: Vue.js 3 + TypeScript SPA (`frontend/`)
- **Vector Store**: ChromaDB persisted to `chroma/` directory
- **Documents**: PDFs stored in `data/docs/` and auto-processed

## Key Design Patterns

### RAG Pipeline Architecture
The system follows a **3-layer RAG pattern**:
1. **Document Processing** (`app/embeddings.py`): PDF → chunks → embeddings → ChromaDB
2. **Retrieval** (`app/rag_pipeline.py`): Query → relevant chunks via similarity search
3. **Generation** (`app/main.py`): Context + query → Ollama Mistral → response

### Vector Storage Strategy
- **Single ChromaDB instance** stores all documents in same vector space (`chroma/`)
- `create_vector_store()` adds new documents to existing Chroma database
- `load_vector_store()` retrieves the entire vector store for querying
- **No document isolation** - all PDFs are searchable together in queries

### External Dependencies
- **Ollama service** must run on host machine (port 11434)
- **Mistral model** used for both embeddings and LLM inference
- Docker backend connects via `host.docker.internal:11434`

## Development Workflows

### Local Development Setup
```bash
# Start Ollama service first (outside Docker)
ollama serve
ollama pull mistral

# Run full stack
docker-compose up
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev  # Vite dev server with hot reload
```

### API Integration Pattern
- **Upload**: `POST /upload` with multipart form data → saves to `data/docs/` → creates embeddings
- **Query**: `GET /ask?query=...` returns `{answer: string}`
- **CORS**: Fully open for development (`allow_origins=["*"]`)
- **No authentication/authorization** - completely open endpoints

## File Organization Conventions

### Backend Structure (`app/`)
- `main.py`: FastAPI routes and CORS setup
- `rag_pipeline.py`: LangChain RetrievalQA chain builder
- `embeddings.py`: ChromaDB operations and PDF processing

### Frontend Structure (`frontend/src/`)
- `App.vue`: Single-page chat interface with file upload (Italian UI text)
- `api.ts`: Axios instance with hardcoded backend URL (`http://localhost:8000`)
- Uses Vue 3 Composition API (`<script setup>`)
- **No routing** - entire app is single component with upload + chat sections

### Data Persistence
- `chroma/`: Vector database files (mounted in Docker)
- `data/docs/`: Uploaded PDFs (mounted in Docker)
- Both directories are **volume-mounted** for persistence

## Critical Implementation Details

### Document Processing Flow
- Upload saves PDF to `data/docs/{filename}` (no validation/sanitization)
- `create_vector_store()` immediately processes with `PyPDFLoader` and creates embeddings
- All documents added to same ChromaDB instance in `chroma/` directory
- **Synchronous processing** - upload blocks until embeddings complete

### Vector Store Loading
- `load_vector_store()` returns entire ChromaDB instance with all documents
- No document filtering - queries search across all uploaded PDFs simultaneously
- Simple implementation but may return results from irrelevant documents

### Error Handling Patterns
- Frontend shows user-friendly Italian messages (`"❌ Errore nel server"`)
- Backend exceptions bubble up as 500 errors
- No structured error responses or logging

### Docker Networking
- Backend needs `extra_hosts` for Ollama access
- Environment variable: `OLLAMA_HOST=host.docker.internal:11434`
- Frontend hardcoded to `http://localhost:8000` (development only)

## Common Modification Points

### Adding New Document Types
1. Update `app/embeddings.py` loader logic beyond `PyPDFLoader`
2. Modify upload endpoint in `app/main.py` for new file types
3. Update frontend file input validation

### Changing LLM/Embeddings Model
1. Update model name in `OllamaLLM(model="...")` and `OllamaEmbeddings(model="...")`
2. Ensure model is pulled: `ollama pull <model-name>`
3. Consider embedding dimension compatibility with existing ChromaDB data

### Multi-Document Querying
- Current limitation: `load_vector_store()` returns all documents in single vector space
- Solution pattern: Implement document metadata filtering or separate collections
- Consider adding document selection UI component for targeted queries

### Production Deployment
- Replace hardcoded `localhost` URLs with environment variables
- Implement proper CORS configuration
- Add authentication/authorization if needed
- Consider Ollama hosting alternatives (API services)