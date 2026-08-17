import hashlib
import math
import re
from langchain_core.embeddings import Embeddings


class LightweightEmbeddings(Embeddings):
    """
    Lightweight deterministic embeddings.
    No PyTorch, Hugging Face, FastEmbed, or API key required.
    """

    dimension = 256

    def _embed(self, text: str):
        vector = [0.0] * self.dimension

        words = re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())

        for word in words:
            digest = hashlib.md5(word.encode()).digest()

            index = int.from_bytes(digest[:4], "little") % self.dimension

            # Deterministic positive/negative contribution
            sign = 1.0 if digest[4] % 2 == 0 else -1.0

            vector[index] += sign

        # Normalize vector
        magnitude = math.sqrt(sum(x * x for x in vector))

        if magnitude > 0:
            vector = [x / magnitude for x in vector]

        return vector

    def embed_documents(self, texts):
        return [self._embed(text) for text in texts]

    def embed_query(self, text):
        return self._embed(text)


def get_embeddings():
    return LightweightEmbeddings()