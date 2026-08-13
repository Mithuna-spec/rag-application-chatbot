RAG Knowledge Assistant

A lightweight Retrieval-Augmented Generation (RAG) application that allows users to upload documents or provide a webpage URL and ask questions about the processed content.

Overview

The application supports:

PDF document ingestion
DOCX document ingestion
TXT document ingestion
Webpage URL ingestion
Document chunking
Hugging Face embeddings
FAISS vector search
Retrieval-Augmented Generation
Groq LLM for answer generation
Source display
Session-based chat using session_id
React frontend
FastAPI backend
Loading and error handling

This application intentionally does not use:

Database
Authentication
User accounts
Technology Stack
Backend
Python
FastAPI
LangChain
FAISS
Hugging Face Sentence Transformers
Groq
Pydantic
Uvicorn
Frontend
React
Vite
Axios
CSS
Vector Store

FAISS

LLM

Groq

Embeddings

Hugging Face Sentence Transformers.

Architecture
Document / URL
      ↓
    Loader
      ↓
 Text Extraction
      ↓
   Chunking
      ↓
  Embeddings
      ↓
    FAISS
      ↓
Similarity Retrieval
      ↓
Relevant Context
      ↓
   Groq LLM
      ↓
Answer + Sources
Frontend Flow
React
  ↓
Axios
  ↓
FastAPI
  ↓
RAG Pipeline
  ↓
Response
  ↓
React UI
Project Structure
rag/
├── app/
│   ├── api/
│   ├── embeddings/
│   ├── ingestion/
│   ├── loaders/
│   ├── llm/
│   ├── rag/
│   ├── retrieval/
│   └── vectorstore/
│
├── data/
│   ├── uploads/
│   └── faiss/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
│
├── main.py
├── requirements.txt
├── .env
└── README.md
Backend Setup

Activate the virtual environment:

.\venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Create a .env file:

GROQ_API_KEY=your_groq_api_key

Do not commit .env to GitHub.

Run Backend

From the project root:

uvicorn main:app --host 127.0.0.1 --port 8000

Backend:

http://127.0.0.1:8000

Swagger API documentation:

http://127.0.0.1:8000/docs
Run Frontend

Open a second terminal:

cd frontend

Install dependencies:

npm install

Start the frontend:

npm run dev

Frontend:

http://localhost:5173

If Vite selects another port, use the URL displayed in the terminal.

API Endpoints
Health Check
GET /
Upload Document
POST /ingest/file

Supported formats:

PDF
DOCX
TXT

The request uses multipart/form-data with the field:

file

Example response:

{
  "message": "Document processed successfully.",
  "filename": "test.pdf",
  "chunks": 23
}
Ingest URL
POST /ingest/url

Request:

{
  "url": "https://example.com"
}
Chat
POST /chat/

Request:

{
  "session_id": "unique-session-id",
  "question": "What is this document about?"
}

Example response:

{
  "session_id": "unique-session-id",
  "question": "What is this document about?",
  "answer": "The document is about...",
  "sources": [
    "data/uploads\\test.pdf"
  ]
}
RAG Workflow
Ingestion
PDF / DOCX / TXT / URL
        ↓
      Loader
        ↓
   Text Extraction
        ↓
      Chunking
        ↓
    Embeddings
        ↓
      FAISS
Question Answering
User Question
      ↓
Query Embedding
      ↓
FAISS Similarity Search
      ↓
Relevant Chunks
      ↓
Context Construction
      ↓
Groq LLM
      ↓
Answer + Sources
How to Use
Start the FastAPI backend.
Start the React frontend.
Open the frontend in your browser.
Upload a PDF, DOCX, or TXT file, or provide a webpage URL.
Wait for successful processing.
Ask a question related to the processed content.
View the generated answer.
View the source used for the answer.
Continue asking questions in the same session.
Testing
Document Ingestion

Test:

PDF
DOCX
TXT

Verify that the application displays:

Document processed successfully.

along with the generated chunk count.

URL Ingestion

Provide a valid webpage URL and verify that the content is successfully processed.

Relevant Question

Ask a question whose answer is clearly present in the processed content.

Paraphrased Question

Ask the same information using different wording to test retrieval quality.

Negative Question

Ask a question whose answer is not present in the processed content.

Expected behavior:

I couldn't find that information in the provided knowledge base.

The assistant should not invent information that is unavailable from the retrieved context.

Error Testing

Test:

Empty question
Unsupported file
Invalid URL
Backend unavailable
Missing knowledge base
Security and Git

Do not commit:

.env
venv/
.venv/
frontend/node_modules/
data/uploads/
data/faiss/

The .env file contains sensitive API credentials.

Runtime files and generated FAISS data should remain local unless intentionally configured otherwise.

Future Improvements

Possible future improvements include:

OCR support for scanned/image-based PDFs
Improved retrieval and reranking
Streaming LLM responses
Persistent multi-user knowledge bases
Authentication for multi-user deployments

These are future improvements and are not required for the current lightweight application.