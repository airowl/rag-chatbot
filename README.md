What does this project do?



This project implements a RAG chatbot that uses an LLM model such as Ollama to answer questions based on previously uploaded PDF files.



What technologies does this project use?



- Python - Programming languages

- FastAPI - Back end system

- ChromaDB - DB vector to save all data embedding

- Docker - Container projects

- Ollama Mistral - LLM used to elaborate the answer

- Vue - Used to create an interface UI



Project flow



- User uploads a PDF file

- Back end receives the file and saves it in the folder

- Ask a question about the file

- Back end calculates the embeddings question

- Search the database for all chunks close to the question

- Create a prompt with the chunk question

- Ollama gives the answer

- Back end gives the answer



What did I learn from this project?



In this project, I learned the basics of how AI can really help in reading the data we upload.



I learned how to upload files, save them, and convert the data into vectors that AI can read.



I learned the concept of embeddings and vector databases, prompt insertion, and LLM processing to generate responses.

Translated with DeepL.com (free version)