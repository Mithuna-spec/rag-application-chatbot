# import os

# from dotenv import load_dotenv
# from langchain_google_genai import GoogleGenerativeAIEmbeddings

# load_dotenv()


# def get_embeddings():
#     api_key = os.getenv("GOOGLE_API_KEY")

#     if not api_key:
#         raise ValueError(
#             "GOOGLE_API_KEY is not set in the environment."
#         )

#     return GoogleGenerativeAIEmbeddings(
#         model="gemini-embedding-001",
#         google_api_key=api_key
#     )


from langchain_huggingface import HuggingFaceEmbeddings


from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings

@lru_cache(maxsize=1)
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )