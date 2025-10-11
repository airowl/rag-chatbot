from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader

CHROMA_PATH = "chroma"

def create_vector_store(pdf_path: str):

    # load PDF document
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    # create embeddings
    embeddings = OllamaEmbeddings(model="mistral-7b-instruct")

    # create database vector store
    vectordb = Chroma.from_documents(docs, embeddings, persist_directory=CHROMA_PATH)
    vectordb.persist()
    return vectordb

def load_vector_store():

    embeddings = OllamaEmbeddings(model="mistral-7b-instruct")
    vectordb = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    return vectordb