from langchain_ollama.llms import OllamaLLM
from langchain.chains import RetrievalQA
from app.embeddings import load_vector_store

def build_rag_pipeline():
    vectordb = load_vector_store()
    retriever = vectordb.as_retriever()

    llm = OllamaLLM(model="mistral")
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa