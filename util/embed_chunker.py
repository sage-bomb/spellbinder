import uuid
import numpy as np
import re
from util.embedding import get_embedding

def smart_sentence_chunk(text: str, max_sentences: int = 3) -> list[str]:
    """
    Split text into sentence chunks, grouping up to max_sentences per chunk.
    """
    # Basic sentence splitter (not NLP-deep, but fast and serviceable)
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    chunks = []

    for i in range(0, len(sentences), max_sentences):
        chunk = " ".join(sentences[i:i + max_sentences]).strip()
        if chunk:
            chunks.append(chunk)

    return chunks


def embed_text_block(text: str, max_sentences: int = 3) -> list[dict]:
    """
    Splits text into chunks and returns:
    [{"eid": <uuid>, "embedding": <np.ndarray>, "text": <original>}]
    """
    segments = smart_sentence_chunk(text, max_sentences=max_sentences)
    result = []

    for segment in segments:
        vec = get_embedding(segment)
        result.append({
            "eid": str(uuid.uuid4()),
            "embedding": np.array(vec, dtype=np.float32),
            "text": segment  # <-- added this
        })

    return result
