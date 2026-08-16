from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.ingest import router as ingest_router
from app.api.chat import router as chat_router


app = FastAPI(
    title="RAG Knowledge Assistant",
    description="Document-based RAG chatbot API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "RAG Knowledge Assistant API is running"
    }