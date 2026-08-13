from pathlib import Path
from urllib.parse import urlparse

from app.loaders.web_loader import load_web_url
from app.loaders.pdf_loader import load_pdf
from app.loaders.docx_loader import load_docx
from app.loaders.text_loader import load_text, load_pasted_text


def is_url(source: str) -> bool:
    parsed = urlparse(source)

    return (
        parsed.scheme in ("http", "https")
        and bool(parsed.netloc)
    )


def add_source_metadata(documents, source, source_type):
    for document in documents:
        document.metadata["source"] = source
        document.metadata["source_type"] = source_type

    return documents


def load_source(source: str):

    # Website
    if is_url(source):
        documents = load_web_url(source)

        return add_source_metadata(
            documents,
            source,
            "web"
        )

    # Local file
    path = Path(source)

    if not path.exists():
        raise FileNotFoundError(
            f"Source not found: {source}"
        )

    extension = path.suffix.lower()

    # PDF
    if extension == ".pdf":
        documents = load_pdf(str(path))

        return add_source_metadata(
            documents,
            path.name,
            "pdf"
        )

    # DOCX
    if extension == ".docx":
        documents = load_docx(str(path))

        return add_source_metadata(
            documents,
            path.name,
            "docx"
        )

    # TXT
    if extension == ".txt":
        documents = load_text(str(path))

        return add_source_metadata(
            documents,
            path.name,
            "txt"
        )

    raise ValueError(
        f"Unsupported file type: {extension}"
    )


def load_text_input(text: str):

    documents = load_pasted_text(text)

    return add_source_metadata(
        documents,
        "pasted_text",
        "text"
    )