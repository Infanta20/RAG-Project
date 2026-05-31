# RAG-Project
Resume RAG Bot
A beginner-friendly Resume Screening RAG Bot built with Streamlit, LangChain, FAISS, and Hugging Face embeddings. Users can upload multiple resume PDFs, search by skills or job requirements, and retrieve the top matching candidates with relevant chunk-level matches.

Features
Upload multiple resume PDFs from the UI.

Extract text from resumes using PDF loaders.

Split resumes into chunks for better retrieval.

Create embeddings using a free/local embedding model. (Hugging Face)

Store and reuse embeddings with FAISS.

Search resumes by skills, keywords, or role requirements.

Display top matching candidates with similarity-based retrieval.

Tech Stack
Frontend/UI: Streamlit

RAG Framework: LangChain

Vector Store: FAISS

Embeddings: Hugging Face Sentence Transformers

PDF Parsing: PyPDF / PyPDFLoader

Language: Python

Project Structure
bash
resume-rag-bot/
│
├── app.py
├── requirements.txt
├── resumes/
├── vectorstore/
└── utils/
    ├── pdf_handler.py
    ├── rag_pipeline.py
    └── ranker.py
Working principle:
Upload one or more resume PDFs in the Streamlit UI.

Save the uploaded files into the resumes/ folder.

Extract text from each PDF.

Split the text into smaller chunks.

Convert chunks into embeddings.

Store embeddings in FAISS inside the vectorstore/ folder.

Ask a skill-based query such as Python, React, SQL.

Retrieve the most relevant chunks and rank matching candidates.

Installation
1. Clone the repository
bash
git clone https://github.com/your-username/resume-rag-bot.git
cd resume-rag-bot
2. Create a virtual environment
Windows (PowerShell):

powershell
py -3.13 -m venv venv
venv\Scripts\activate

3. Install dependencies
bash
python -m pip install -r requirements.txt
4. Run the app
bash
streamlit run app.py
Example Usage
Upload 2 or more resumes.

Click the button that processes resumes.

Wait for chunking, embedding, and FAISS storage to complete.

Enter required skills such as:

Python, Machine Learning, NLP

React, Node.js, MongoDB

Java, Spring Boot, SQL

Choose:

Number of top candidates to show

Number of chunk matches to retrieve

View the ranked candidates.


Learning Goals
This project is useful for learning:

Document ingestion

Text chunking

Embeddings

Vector databases

Retrieval-Augmented Generation (RAG)

Streamlit app building

Practical GenAI portfolio development
