# 🧠 RAG Knowledge Assistant

A lightweight, high-performance **Retrieval-Augmented Generation (RAG)** application designed to ingest documents or web pages and answer context-aware questions seamlessly. Built with a **FastAPI** backend and a modern **React + Vite** frontend, powered by **Groq LLM**, **LangChain**, and **FAISS**.

---

## 🚀 Key Features

* **Multi-Format Ingestion:** Supports PDF, DOCX, TXT files, and live Webpage URLs.
* **Smart Chunking & Embeddings:** Uses Hugging Face Sentence Transformers for robust vector representations.
* **Fast Vector Search:** Powered by FAISS for rapid similarity retrieval.
* **LLM-Powered Responses:** Utilizes Groq for lightning-fast answer generation with strict grounding against hallucinations.
* **Session-Based Chat:** Maintains conversational context using unique `session_id` tracking.
* **Transparent Citations:** Automatically displays source documents/URLs alongside answers.

---

## 🛠️ Technology Stack

### **Backend**
* **Framework:** Python, FastAPI, Uvicorn
* **Orchestration & RAG:** LangChain, Pydantic
* **Vector Store & Embeddings:** FAISS, Hugging Face Sentence Transformers
* **LLM:** Groq API

### **Frontend**
* **Library:** React, Vite
* **HTTP Client:** Axios
* **Styling:** CSS

---

## 📂 Project Structure

```text
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
├── data/
│   ├── uploads/
│   └── faiss/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
├── main.py
├── requirements.txt
├── .env
└── README.md

⚙️ Getting Started & Installation1. Backend SetupNavigate to the root directory, activate your virtual environment, and install dependencies:Bash# Activate virtual environment
# Windows:
.\venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
Create a .env file in the project root and add your Groq API key:Code snippetGROQ_API_KEY=your_groq_api_key_here
⚠️ Security Warning: Never commit your .env file to version control.2. Frontend SetupOpen a separate terminal window and navigate to the frontend directory:Bashcd frontend

# Install dependencies
npm install
🏃‍♂️ Running the ApplicationStart the BackendFrom the project root directory:Bashuvicorn main:app --host 127.0.0.1 --port 8000 --reload
Backend API: http://127.0.0.1:8000Swagger Documentation: http://127.0.0.1:8000/docsStart the FrontendFrom the frontend directory:Bashnpm run dev
Frontend App: http://localhost:5173 (or check terminal for alternative Vite ports)🔌 API Endpoints ReferenceEndpointMethodRequest Payload / ParamsDescription/GETNoneHealth check endpoint/ingest/filePOSTmultipart/form-data (file)Ingests PDF, DOCX, or TXT documents/ingest/urlPOST{"url": "https://example.com"}Scrapes and ingests a webpage URL/chat/POST{"session_id": "string", "question": "string"}Submits a query and returns an LLM answer with sourcesExample Ingestion Response (POST /ingest/file)JSON{
  "message": "Document processed successfully.",
  "filename": "test.pdf",
  "chunks": 23
}
Example Chat Response (POST /chat/)JSON{
  "session_id": "unique-session-id",
  "question": "What is this document about?",
  "answer": "The document details...",
  "sources": ["data/uploads/test.pdf"]
}
🔄 Architecture & WorkflowIngestion FlowPlaintextPDF / DOCX / TXT / URL 
       ↓
    Loader 
       ↓
 Text Extraction 
       ↓
   Chunking 
       ↓
   Embeddings 
       ↓
  FAISS Vector Store
Question Answering FlowPlaintextUser Question 
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
🧪 Testing GuideDocument Ingestion: Upload sample PDF, DOCX, and TXT files. Verify success messages and chunk counts.URL Ingestion: Submit a valid article or documentation URL.Relevant Questions: Ask direct questions whose answers exist in your knowledge base.Paraphrased Questions: Rephrase the same queries using alternative wording to test retrieval robustness.Negative Question Testing: Ask questions outside the scope of your uploaded content.Expected Output: "I couldn't find that information in the provided knowledge base." (The system should strictly avoid hallucination).Error Handling: Test edge cases such as empty questions, invalid URLs, unsupported file types, and queries submitted without an active knowledge base.🛡️ Security & Git Best PracticesEnsure the following patterns are included in your .gitignore to keep sensitive credentials and volatile runtime data out of source control:Code snippet.env
venv/
.venv/
frontend/node_modules/
data/uploads/
data/faiss/
dist/