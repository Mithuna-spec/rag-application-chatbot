from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil

from app.loaders.pdf_loader import load_pdf
from app.loaders.docx_loader import load_docx
from app.loaders.text_loader import load_text
from app.ingestion.splitter import split_documents
from app.embeddings.embedding_service import get_embeddings
from app.vectorstore.knowledge_base import (
    create_knowledge_base,
    save_knowledge_base,
    clear_knowledge_base
)
from pydantic import BaseModel, HttpUrl
from app.loaders.web_loader import load_web_url


router = APIRouter(
    prefix="/ingest",
    tags=["Ingestion"]
)


UPLOAD_DIR = "data/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/file")
async def ingest_file(file: UploadFile = File(...)):

    filename = file.filename

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided."
        )

    extension = os.path.splitext(filename)[1].lower()

    allowed_extensions = {
        ".pdf",
        ".docx",
        ".txt"
    }

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX and TXT files are supported."
        )

    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 1. Load document
    if extension == ".pdf":
        documents = load_pdf(file_path)

    elif extension == ".docx":
        documents = load_docx(file_path)

    else:
        documents = load_text(file_path)

    # Calculate text length across all documents to check for scanned warning
    total_text_length = sum(len(doc.page_content) for doc in documents)
    
    if extension == ".pdf" and total_text_length < 200:
        print("\n⚠️ WARNING: PDF may be scanned/image-based or contain little extractable text.")
        print(f"Extracted characters: {total_text_length}\n")

    # 2. Split into chunks
    chunks = split_documents(documents)

    # 3. Create embeddings
    embeddings = get_embeddings()

    clear_knowledge_base("data/faiss")

    # 4. Create FAISS vector store
    vectorstore = create_knowledge_base(
        chunks,
        embeddings
    )

    # 5. Save FAISS
    save_knowledge_base(
        vectorstore,
        "data/faiss"
    )

    # Print Ingestion Debug
    print("\n===== INGESTION DEBUG =====")
    print(f"Filename: {filename}")
    print(f"Number of extracted documents (pages): {len(documents)}")
    print(f"Total extracted text length: {total_text_length} characters")
    if documents:
        print(f"First 200 characters: {repr(documents[0].page_content[:200])}")
        print(f"Source metadata: {documents[0].metadata}")
    print(f"Number of generated chunks: {len(chunks)}")
    print(f"Chunk lengths: {[len(c.page_content) for c in chunks]}")
    print(f"FAISS vector count (index size): {vectorstore.index.ntotal}")
    print("===========================\n")

    return {
        "message": "Document processed successfully.",
        "filename": filename,
        "chunks": len(chunks)
    }



class URLRequest(BaseModel):
    url: HttpUrl

@router.post("/url")
def ingest_url(request: URLRequest):

    url = str(request.url)

    # 1. Load webpage
    documents = load_web_url(url)

    if not documents:
        raise HTTPException(
            status_code=400,
            detail="No content could be loaded from the URL."
        )

    # 2. Split into chunks
    chunks = split_documents(documents)

    if not chunks:
        raise HTTPException(
            status_code=400,
            detail="No chunks were created from the URL."
        )

    # 3. Create embeddings
    embeddings = get_embeddings()

    clear_knowledge_base("data/faiss")

    # 4. Create FAISS vector store
    vectorstore = create_knowledge_base(
        chunks,
        embeddings
    )

    # 5. Save FAISS
    save_knowledge_base(
        vectorstore,
        "data/faiss"
    )

    total_text_length = sum(len(doc.page_content) for doc in documents)
    
    # Print Ingestion Debug
    print("\n===== INGESTION DEBUG =====")
    print(f"URL: {url}")
    print(f"Number of extracted documents: {len(documents)}")
    print(f"Total extracted text length: {total_text_length} characters")
    if documents:
        print(f"First 200 characters: {repr(documents[0].page_content[:200])}")
        print(f"Source metadata: {documents[0].metadata}")
    print(f"Number of generated chunks: {len(chunks)}")
    print(f"Chunk lengths: {[len(c.page_content) for c in chunks]}")
    print(f"FAISS vector count (index size): {vectorstore.index.ntotal}")
    print("===========================\n")

    return {
        "message": "URL processed successfully.",
        "url": url,
        "chunks": len(chunks)
    }