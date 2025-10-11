from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from app.embeddings import load_vector_store

def build_rag_pipeline():
    vectordb = load_vector_store()
    