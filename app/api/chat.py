from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys

def safe_print(text: str):
    try:
        print(text)
    except UnicodeEncodeError:
        encoding = sys.stdout.encoding or 'utf-8'
        print(text.encode(encoding, errors='replace').decode(encoding))


from app.embeddings.embedding_service import get_embeddings
from app.vectorstore.knowledge_base import load_knowledge_base
from app.llm.llm_service import get_llm

from app.chat.chat_service import (
    create_chat_session,
    add_message,
    format_chat_history
)

from app.chat.session_store import sessions
from app.retrieval.retriever import retrieve_documents


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):
    question: str
    session_id: str = "default"


@router.post("/")
def chat(request: ChatRequest):

    # -----------------------------------------
    # 1. Validate question
    # -----------------------------------------

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    # -----------------------------------------
    # 2. Get or create chat session
    # -----------------------------------------

    if request.session_id not in sessions:
        sessions[request.session_id] = create_chat_session()

    history = sessions[request.session_id]

    chat_history = format_chat_history(history)

    # -----------------------------------------
    # 3. Load embeddings
    # -----------------------------------------

    embeddings = get_embeddings()

    # -----------------------------------------
    # 4. Load FAISS knowledge base
    # -----------------------------------------

    try:
        vectorstore = load_knowledge_base(
            embeddings,
            "data/faiss"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Knowledge base could not be loaded: {str(e)}"
        )

    # -----------------------------------------
    # 5. Retrieve relevant documents
    # -----------------------------------------

    try:
        documents = retrieve_documents(
            vectorstore,
            request.question,
            k=5
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Document retrieval failed: {str(e)}"
        )

    # Print Retrieval Debug
    print("\n===== RETRIEVAL DEBUG =====")
    safe_print(f"Question:\n{request.question}\n")
    print("Retrieved documents:")
    for idx, doc in enumerate(documents):
        print(f"--- RESULT {idx + 1} ---")
        safe_print(doc.page_content)
        safe_print(f"Source:\n{doc.metadata.get('source', 'Unknown')}\n")
    print("===========================\n")

    if not documents:
        raise HTTPException(
            status_code=404,
            detail="No relevant information found in the knowledge base."
        )

    # -----------------------------------------
    # 6. Build context
    # -----------------------------------------

    context = "\n\n".join(
        doc.page_content
        for doc in documents
    )

    # -----------------------------------------
    # 7. Get LLM
    # -----------------------------------------

    try:
        llm = get_llm()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLM could not be initialized: {str(e)}"
        )

    # -----------------------------------------
    # 8. Generic RAG prompt
    # -----------------------------------------

    prompt = f"""
You are a knowledge assistant.

Answer the user's question using ONLY the information
contained in the provided context.

Do not use outside knowledge.

Do not make up facts.

Use the previous conversation only to understand
references or follow-up questions.

If the answer cannot be found in the provided context,
say exactly:

"I couldn't find that information in the provided knowledge base."

Previous conversation:
{chat_history}

Context:
{context}

Current question:
{request.question}

Answer:
"""

    # -----------------------------------------
    # 9. Generate answer
    # -----------------------------------------

    try:
        response = llm.invoke(prompt)

        answer = response.content

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate answer: {str(e)}"
        )

    # -----------------------------------------
    # 10. Save conversation
    # -----------------------------------------

    add_message(
        history,
        request.question,
        answer
    )

    # -----------------------------------------
    # 11. Collect sources
    # -----------------------------------------

    sources = []

    for doc in documents:

        source = doc.metadata.get(
            "source",
            "Unknown"
        )

        if source not in sources:
            sources.append(source)

    # -----------------------------------------
    # 12. Return response
    # -----------------------------------------

    return {
        "session_id": request.session_id,
        "question": request.question,
        "answer": answer,
        "sources": sources
    }