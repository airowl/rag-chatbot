from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import shutil
from app.embeddings import create_vector_store
from app.rag_pipeline import build_rag_pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_pdf(file: UploadFile):
    path = f"data/docs/{file.filename}"
    
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    create_vector_store(path)
    return {"message": f"File {file.filename} uploaded and processed."}

@app.get("/ask")
async def ask(query: str):
    qa = build_rag_pipeline()
    response = qa.run(query)
    return {"answer": response}