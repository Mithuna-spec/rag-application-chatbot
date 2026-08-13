from fastapi import FastAPI

from app.api.ingest import router as ingest_router
from app.api.chat import router as chat_router


app = FastAPI(
    title="RAG Knowledge Assistant",
    description="Document-based RAG chatbot API",
    version="1.0.0"
)

app.include_router(ingest_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "RAG Knowledge Assistant API is running"
    }