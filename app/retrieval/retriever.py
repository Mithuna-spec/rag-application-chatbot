from langchain_core.documents import Document


def retrieve_documents(
    vectorstore,
    question: str,
    k: int = 5,
    chat_history: str = ""
) -> list[Document]:

    if not question.strip():
        return []

    # Add conversation context so follow-up questions
    # such as "what is the source about?" can be understood.
    if chat_history.strip():
        retrieval_query = f"""
Previous conversation:
{chat_history}

Current question:
{question}
"""
    else:
        retrieval_query = question

    documents = vectorstore.similarity_search(
        query=retrieval_query,
        k=k
    )

    return documents