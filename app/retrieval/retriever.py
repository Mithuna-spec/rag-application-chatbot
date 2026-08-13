from langchain_core.documents import Document


def retrieve_documents(
    vectorstore,
    question: str,
    k: int = 5
) -> list[Document]:

    if not question.strip():
        return []

    documents = vectorstore.similarity_search(
        query=question,
        k=k
    )

    return documents