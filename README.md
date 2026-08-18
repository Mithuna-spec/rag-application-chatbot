<div align="center">

# 🧠 RAG Knowledge Assistant

**A lightweight, high-performance Retrieval-Augmented Generation (RAG) application**
that ingests documents and web pages, then answers context-aware questions — with full source citations and zero hallucination tolerance.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-Build%20Tool-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![LangChain](https://img.shields.io/badge/LangChain-Orchestration-1C3C3C)](https://www.langchain.com/)
[![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-0467DF)](https://github.com/facebookresearch/faiss)
[![Groq](https://img.shields.io/badge/Groq-LLM%20Inference-F55036)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#-contributing)

[Features](#-key-features) •
[Tech Stack](#-technology-stack) •
[Quick Start](#-getting-started--installation) •
[API Reference](#-api-endpoints-reference) •
[Architecture](#-architecture--workflow) •
[Testing](#-testing-guide) •
[Contributing](#-contributing)

</div>

---

## 📖 Overview

**RAG Knowledge Assistant** turns your documents and web pages into a queryable knowledge base. Upload a PDF, DOCX, or TXT file — or point it at a URL — and ask natural-language questions grounded strictly in that content. Under the hood, a **FastAPI** backend handles ingestion, chunking, embedding, and retrieval via **FAISS**, while **Groq** powers fast, low-latency LLM responses. A **React + Vite** frontend provides a clean, responsive chat interface with session tracking and transparent source citations.

---

## 🚀 Key Features

| Feature | Description |
|---|---|
| 📄 **Multi-Format Ingestion** | Supports PDF, DOCX, TXT files, and live webpage URLs |
| ✂️ **Smart Chunking & Embeddings** | Uses Hugging Face Sentence Transformers for robust vector representations |
| ⚡ **Fast Vector Search** | Powered by FAISS for rapid similarity retrieval |
| 🤖 **LLM-Powered Responses** | Utilizes Groq for lightning-fast answer generation with strict grounding against hallucinations |
| 💬 **Session-Based Chat** | Maintains conversational context using unique `session_id` tracking |
| 🔗 **Transparent Citations** | Automatically displays source documents/URLs alongside every answer |

---

## 🛠️ Technology Stack

### Backend
| Component | Technology |
|---|---|
| Framework | Python, FastAPI, Uvicorn |
| Orchestration & RAG | LangChain, Pydantic |
| Vector Store & Embeddings | FAISS, Hugging Face Sentence Transformers |
| LLM Provider | Groq API |

### Frontend
| Component | Technology |
|---|---|
| Library | React, Vite |
| HTTP Client | Axios |
| Styling | CSS |

---

## 📂 Project Structure

```text
rag/
├── app/
│   ├── api/            # FastAPI route definitions
│   ├── embeddings/     # Embedding model logic
│   ├── ingestion/       # File/URL ingestion pipeline
│   ├── loaders/         # Format-specific document loaders
│   ├── llm/              # Groq LLM integration
│   ├── rag/              # Core RAG orchestration (LangChain)
│   ├── retrieval/       # Similarity search & context building
│   └── vectorstore/     # FAISS index management
├── data/
│   ├── uploads/          # Uploaded source documents
│   └── faiss/             # Persisted FAISS indexes
├── frontend/
│   ├── src/
│   │   ├── components/  # React UI components
│   │   ├── services/      # API client (Axios) layer
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
├── main.py                # FastAPI application entrypoint
├── requirements.txt
├── .env                    # Environment variables (not committed)
└── README.md
```

---

## ✅ Prerequisites

Before you begin, ensure you have the following installed:

- **Python** 3.10 or higher
- **Node.js** 18+ and **npm**
- A **Groq API key** — [get one here](https://console.groq.com/)
- **Git** (for cloning the repository)

---

## ⚙️ Getting Started & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/rag-knowledge-assistant.git
cd rag-knowledge-assistant
```

### 2. Backend Setup

Create and activate a virtual environment from the project root:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> ⚠️ **Security Warning:** Never commit your `.env` file to version control. Ensure it is listed in `.gitignore` (see [Security & Git Best Practices](#-security--git-best-practices)).

### 3. Frontend Setup

Open a separate terminal and navigate to the frontend directory:

```bash
cd frontend
npm install
```

---

## 🏃 Running the Application

### Start the Backend

From the project root directory:

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

| Resource | URL |
|---|---|
| Backend API | http://127.0.0.1:8000 |
| Swagger Documentation | http://127.0.0.1:8000/docs |

### Start the Frontend

From the `frontend` directory:

```bash
npm run dev
```

| Resource | URL |
|---|---|
| Frontend App | http://localhost:5173 (or check terminal for alternative Vite ports) |

---

## 🔌 API Endpoints Reference

| Endpoint | Method | Request Payload / Params | Description |
|---|---|---|---|
| `/` | `GET` | None | Health check endpoint |
| `/ingest/file` | `POST` | `multipart/form-data` (`file`) | Ingests PDF, DOCX, or TXT documents |
| `/ingest/url` | `POST` | `{ "url": "https://example.com" }` | Scrapes and ingests a webpage URL |
| `/chat/` | `POST` | `{ "session_id": "string", "question": "string" }` | Submits a query and returns an LLM answer with sources |

### Example: Ingestion Response (`POST /ingest/file`)

```json
{
  "message": "Document processed successfully.",
  "filename": "test.pdf",
  "chunks": 23
}
```

### Example: Chat Response (`POST /chat/`)

```json
{
  "session_id": "unique-session-id",
  "question": "What is this document about?",
  "answer": "The document details...",
  "sources": ["data/uploads/test.pdf"]
}
```

---

## 🔄 Architecture & Workflow

### Ingestion Flow

```text
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
 FAISS Vector Store
```

### Question Answering Flow

```text
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
```

---

## 🧪 Testing Guide

| Test Case | Description | Expected Outcome |
|---|---|---|
| **Document Ingestion** | Upload sample PDF, DOCX, and TXT files | Success message with accurate chunk counts |
| **URL Ingestion** | Submit a valid article or documentation URL | Page content is scraped and indexed |
| **Relevant Questions** | Ask direct questions whose answers exist in the knowledge base | Accurate, grounded answers with sources |
| **Paraphrased Questions** | Rephrase the same queries using alternative wording | Consistent retrieval and correct answers |
| **Negative Question Testing** | Ask questions outside the scope of uploaded content | `"I couldn't find that information in the provided knowledge base."` (no hallucination) |
| **Error Handling** | Test empty questions, invalid URLs, unsupported file types, and queries with no active knowledge base | Graceful, descriptive error responses |

---

## 🛡️ Security & Git Best Practices

Ensure the following patterns are included in your `.gitignore` to keep sensitive credentials and volatile runtime data out of source control:

```gitignore
.env
venv/
.venv/
frontend/node_modules/
data/uploads/
data/faiss/
dist/
```

**Additional recommendations:**
- Rotate your Groq API key periodically and never share it publicly.
- Avoid logging raw user documents or PII in production environments.
- Validate and sanitize all uploaded files and URLs before ingestion.
- Use HTTPS in production deployments to protect data in transit.

---

## 🗺️ Roadmap

- [ ] Support for additional file formats (Markdown, CSV, JSON)
- [ ] Streaming responses for real-time answer generation
- [ ] Multi-user authentication and access control
- [ ] Configurable chunking strategies and embedding models
- [ ] Docker Compose setup for one-command deployment

---

## 🤝 Contributing

Contributions are welcome and appreciated! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code follows existing style conventions and includes relevant tests where applicable.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [LangChain](https://www.langchain.com/) for RAG orchestration
- [FAISS](https://github.com/facebookresearch/faiss) by Meta AI for vector search
- [Groq](https://groq.com/) for high-speed LLM inference
- [Hugging Face](https://huggingface.co/) for Sentence Transformer embeddings

---

<div align="center">

Made with ❤️ using FastAPI, React, and Groq

</div>
