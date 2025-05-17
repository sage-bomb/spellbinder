import numpy as np
from typing import List, Dict

class VectorSearchIndex:
    def __init__(self):
        self.index: Dict[str, np.ndarray] = {}

    def add_many(self, items: List[Dict[str, any]]):
        for item in items:
            vec = item["embedding"]
            vec = np.array(vec, dtype=np.float32)

            if vec.ndim != 1:
                raise ValueError(f"Embedding for {item['eid']} is not 1D: shape={vec.shape}")

            self.index[item["eid"]] = vec


    def add_one(self, eid: str, embedding: np.ndarray):
        self.index[eid] = embedding

    def search(self, query: np.ndarray, top_k: int = 5) -> List[Dict[str, float]]:
        if not self.index:
            return []

        all_keys = list(self.index.keys())
        all_vectors = np.stack([self.index[k] for k in all_keys])

        # Normalize vectors
        query_norm = query / np.linalg.norm(query)
        vecs_norm = all_vectors / np.linalg.norm(all_vectors, axis=1, keepdims=True)

        # Cosine similarity = dot product of normalized vectors
        scores = np.dot(vecs_norm, query_norm)
        top_indices = np.argsort(scores)[::-1][:top_k]

        return [
            {"eid": all_keys[i], "score": float(scores[i])}
            for i in top_indices
        ]
