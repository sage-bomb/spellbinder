
import os
import json
import numpy as np
from typing import List, Union
from sentence_transformers import SentenceTransformer



# Load once on import
_model = SentenceTransformer("BAAI/bge-base-en")

def get_embedding(text: str):
    return _model.encode(text, normalize_embeddings=True).tolist()


DATA_DIR = "data/embeddings/"

def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def save_embeddings(name: str, embeddings: List[List[float]], metadata: Union[List[dict], None] = None):
    _ensure_data_dir()
    path = os.path.join(DATA_DIR, f"{name}.npz")
    np.savez_compressed(path, embeddings=np.array(embeddings, dtype=np.float32))
    
    if metadata:
        with open(os.path.join(DATA_DIR, f"{name}_meta.json"), "w") as f:
            json.dump(metadata, f, indent=2)
    print(f"✅ Saved {len(embeddings)} embeddings to {path}")

def delete_embedding(uid: str, silent: bool = False):
    vec_path = os.path.join(DATA_DIR, f"{uid}.npz")
    meta_path = os.path.join(DATA_DIR, f"{uid}_meta.json")

    if os.path.exists(vec_path):
        os.remove(vec_path)
        if not silent:
            print(f"🗑️ Deleted vector file: {vec_path}")
    elif not silent:
        print(f"⚠️ No vector file found for UUID: {uid}")

    if os.path.exists(meta_path):
        os.remove(meta_path)
        if not silent:
            print(f"🗑️ Deleted metadata file: {meta_path}")
    elif not silent:
        print(f"⚠️ No metadata file found for UUID: {uid}")


def save_embedding(uid: str, embedding: List[float]):
    _ensure_data_dir()
    path = os.path.join(DATA_DIR, f"{uid}.npz")
    np.savez_compressed(path, embedding=np.array(embedding, dtype=np.float32))

def load_embedding(uid: str) -> np.ndarray:
    path = os.path.join(DATA_DIR, f"{uid}.npz")
    if not os.path.exists(path):
        raise FileNotFoundError(f"No embedding file found at {path}")
    return np.load(path)["embedding"]



def load_embeddings(name: str):
    embed_path = os.path.join(DATA_DIR, f"{name}.npz")
    meta_path = os.path.join(DATA_DIR, f"{name}_meta.json")

    if not os.path.exists(embed_path):
        raise FileNotFoundError(f"No embedding file found at {embed_path}")

    embeddings = np.load(embed_path)["embeddings"]

    metadata = None
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            metadata = json.load(f)

    return embeddings, metadata

