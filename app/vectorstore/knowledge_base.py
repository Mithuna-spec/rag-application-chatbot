from pathlib import Path

from langchain_community.vectorstores import FAISS
from app.ingestion.ingestion_service import load_source


def create_knowledge_base(chunks, embeddings):
    return FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )


def save_knowledge_base(vectorstore, path="data/faiss"):
    Path(path).mkdir(parents=True, exist_ok=True)

    vectorstore.save_local(path)

    # Save model metadata for safety validation checks
    import json
    model_name = getattr(vectorstore.embedding_function, "model_name", None)
    if not model_name:
        model_name = vectorstore.embedding_function.__class__.__name__

    model_info = {
        "embedding_model": model_name
    }
    with open(Path(path) / "model_info.json", "w") as f:
        json.dump(model_info, f)


def load_knowledge_base(embeddings, path="data/faiss"):
    import json
    model_info_path = Path(path) / "model_info.json"
    if model_info_path.exists():
        try:
            with open(model_info_path, "r") as f:
                info = json.load(f)
            expected_model = info.get("embedding_model")
            current_model = getattr(embeddings, "model_name", None) or embeddings.__class__.__name__
            if expected_model and current_model and expected_model != current_model:
                raise ValueError(
                    f"Embedding model mismatch! The FAISS index was created using '{expected_model}', "
                    f"but the current application is configured to use '{current_model}'."
                )
        except Exception as e:
            if isinstance(e, ValueError):
                raise e
            print(f"Warning: Failed to read model metadata: {e}")

    vectorstore = FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore



def create_knowledge_base_from_sources(
    sources,
    embeddings,
    splitter
):
    all_documents = []

    for source in sources:
        documents = load_source(source)
        all_documents.extend(documents)

    chunks = splitter(all_documents)

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return vectorstore, chunks

import shutil


def clear_knowledge_base(path="data/faiss"):
    path = Path(path)

    if path.exists():
        shutil.rmtree(path)