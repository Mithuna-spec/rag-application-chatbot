from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document


def load_text(file_path: str):
    loader = TextLoader(
        file_path,
        encoding="utf-8"
    )
    return loader.load()


def load_pasted_text(text: str):
    return [
        Document(
            page_content=text,
            metadata={"source": "pasted_text"}
        )
    ]