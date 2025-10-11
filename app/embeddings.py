from langchain_ollama import OllamaEmbeddings
from langchain_chroma.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader

CHROMA_PATH = "chroma"

def create_vector_store(pdf_path: str):

    # load PDF document
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    # create embeddings
    embeddings = OllamaEmbeddings(model="mistral")

    # create database vector store
    vectordb = Chroma(collection_name=docs[0].metadata["source"], embedding_function=embeddings, persist_directory=CHROMA_PATH)
    return vectordb

def load_vector_store():
    #  load DB
    embeddings = OllamaEmbeddings(model="mistral")
    vectordb = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    return vectordb