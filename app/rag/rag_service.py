from app.chat.chat_service import format_chat_history
def format_context(documents):
    context_parts = []

    for doc in documents:
        source = doc.metadata.get("source", "Unknown source")

        context_parts.append(
            f"Source: {source}\n"
            f"Content: {doc.page_content}"
        )

    return "\n\n".join(context_parts)


def generate_rag_answer(question, retriever, llm):
    documents = retriever.invoke(question)

    context = format_context(documents)

    prompt = f"""
You are a knowledge assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:
"I couldn't find that information in the provided knowledge base."

Do not use your general knowledge to answer unsupported questions.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    sources = []

    for doc in documents:
        source = doc.metadata.get("source")

        if source and source not in sources:
            sources.append(source)

    return {
        "answer": response.content,
        "sources": sources,
        "documents": documents
    }

def generate_chat_rag_answer(
    question,
    retriever,
    llm,
    chat_history
):
    documents = retriever.invoke(question)

    context_parts = []

    for doc in documents:
        source = doc.metadata.get(
            "source",
            "Unknown source"
        )

        context_parts.append(
            f"Source: {source}\n"
            f"Content: {doc.page_content}"
        )

    context = "\n\n".join(context_parts)

    history = format_chat_history(chat_history)

    prompt = f"""
You are a knowledge assistant.

Answer the user's question using ONLY the provided knowledge base context.

You may use the conversation history to understand
what the user is referring to.

Do not use general knowledge to invent information.

If the answer cannot be found in the provided context,
say:

"I couldn't find that information in the provided knowledge base."

Conversation history:
{history}

Knowledge base context:
{context}

Current question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    sources = []

    for doc in documents:
        source = doc.metadata.get("source")

        if source and source not in sources:
            sources.append(source)

    return {
        "answer": response.content,
        "sources": sources,
        "documents": documents
    }