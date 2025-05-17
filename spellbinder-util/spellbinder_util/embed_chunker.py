import uuid
import numpy as np
import re
from spellbinder_util.embedding import get_embedding

def smart_semantic_chunk(text: str, max_tokens: int = 512) -> list[str]:
    """
    Smart novel-optimized chunker:
    - First split by paragraph (\n\n)
    - Treat dialogue blocks as atomic
    - Greedy pack paragraphs into chunks up to max_tokens
    """
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""

    dialogue_pattern = re.compile(r'(“[^”]+”|"[^"]+"|‘[^’]+’|\'[^\']+\')')

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # Treat pure dialogue block as atomic
        if dialogue_pattern.fullmatch(para):
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""
            chunks.append(para)
            continue

        temp_chunk = (current_chunk + "\n\n" + para).strip() if current_chunk else para

        # crude token approximation (1 word ~ 1 token)
        if len(temp_chunk.split()) > max_tokens:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para
        else:
            current_chunk = temp_chunk

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def split_narrative(text: str, max_tokens: int) -> list[str]:
    """
    Split narrative text by sentence boundaries and token estimate.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    current_chunk = ''
    output = []

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        temp = (current_chunk + ' ' + sentence).strip()

        # crude token approximation (1 word ~ 1 token)
        if len(temp.split()) > max_tokens:
            if current_chunk:
                output.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk = temp

    if current_chunk:
        output.append(current_chunk.strip())

    return output

from sklearn.metrics.pairwise import cosine_similarity

def evaluate_embedding_diversity(embeddings, similarity_threshold=0.95):
    if len(embeddings) < 2:
        return True  # not enough to evaluate
    similarity_matrix = cosine_similarity(embeddings)
    np.fill_diagonal(similarity_matrix, 0)
    mean_similarity = similarity_matrix.mean()
    return mean_similarity < similarity_threshold

def embed_text_block(text: str,file_eid: str, max_tokens: int = 512) -> list[dict]:
    """
    Splits text into improved semantic chunks and returns:
    [{"eid": <uuid>, "embedding": <np.ndarray>, "text": <original>}]
    """
    for attempt in range(3):
        segments = smart_semantic_chunk(text, max_tokens=max_tokens)
        embeddings = [get_embedding(seg) for seg in segments]
        if evaluate_embedding_diversity(embeddings):
            best_chunks = segments
            break
        max_tokens = int(max_tokens * 1.2)  # increase chunk size and try again
    result = []
    for segment, vec in zip(best_chunks, embeddings):
    
        
            result.append({
                "eid": str(uuid.uuid4()),
                "file_eid": file_eid, 
                "embedding": np.array(vec, dtype=np.float32),
                "text": segment
            })

    return result
