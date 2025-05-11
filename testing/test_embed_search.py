import os
import uuid
import numpy as np

from util.embed_chunker import embed_text_block
from util.vector_search import VectorSearchIndex
from util.embedding import (
    get_embedding,
    save_embedding,
    load_embedding,
    delete_embedding
)
from util.embedding_store import EmbeddingStore
import json

EMBEDDING_DIR = "data/embeddings"

def load_existing_embeddings():
    eid_to_text = {}
    index = VectorSearchIndex()
    index_file = os.path.join(EMBEDDING_DIR, "index.json")

    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            eid_to_text = json.load(f)

    for eid in eid_to_text:
        vec = load_embedding(eid)
        if vec is not None and vec.ndim == 1:
            index.add_one(eid, vec)

    print(f"✅ Loaded {len(eid_to_text)} embeddings from disk.")
    return eid_to_text, index

def embed_new_documents(memory_only, store, directory_path):
    eid_to_text = {}
    saved_eids = []
    index = VectorSearchIndex()

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if not os.path.isfile(file_path):
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = embed_text_block(text)

        for chunk in chunks:
            eid = chunk["eid"]
            vec = np.array(chunk["embedding"], dtype=np.float32)

            if vec.ndim != 1:
                print(f"⚠️ Skipping malformed embedding for eid={eid}: shape={vec.shape}")
                continue

            eid_to_text[eid] = {"text": chunk["text"], "file": filename}
            saved_eids.append(eid)

            if memory_only:
                store.save(eid, vec)
                index.add_one(eid, vec)
            else:
                save_embedding(eid, vec)

    if not memory_only:
        os.makedirs(EMBEDDING_DIR, exist_ok=True)
        with open(os.path.join(EMBEDDING_DIR, "index.json"), "w", encoding="utf-8") as f:
            json.dump(eid_to_text, f, indent=2)
        index.add_many([{ "eid": eid, "embedding": load_embedding(eid) } for eid in eid_to_text])

    print(f"✅ {'Stored in memory' if memory_only else 'Embedded and saved'} {len(eid_to_text)} segments from {directory_path}.")
    return eid_to_text, saved_eids, index

def compute_mrr(rank_list, expected_file, eid_to_text):
    for rank, hit in enumerate(rank_list, start=1):
        if eid_to_text[hit["eid"]]["file"] == expected_file:
            return 1.0 / rank
    return 0.0

def compute_ndcg(rank_list, expected_file, eid_to_text, k=5):
    dcg = 0.0
    for i, hit in enumerate(rank_list[:k]):
        rel = 1 if eid_to_text[hit["eid"]]["file"] == expected_file else 0
        dcg += rel / np.log2(i + 2)

    idcg = 1.0  # ideal DCG if perfect hit at rank 1
    return dcg / idcg

def test_directory_embedding_search(memory_only: bool = False, load_existing: bool = False, cleanup: bool = True):

    eid_to_text = {}
    saved_eids = []
    index = VectorSearchIndex()
    store = EmbeddingStore() if memory_only else None
    directory_path = "../test_docs/test_search"

    is_fresh_run = not load_existing

    if load_existing:
        index_file = os.path.join(EMBEDDING_DIR, "index.json")
        embeddings_exist = os.path.exists(index_file) and len(os.listdir(EMBEDDING_DIR)) > 0
        if embeddings_exist:
            eid_to_text, index = load_existing_embeddings()
        else:
            is_fresh_run = True

    if is_fresh_run:
        eid_to_text, saved_eids, index = embed_new_documents(memory_only, store, directory_path)

    # Test with dataset
    dataset_file = "embedding_test_data.json"
    if os.path.exists(dataset_file):
        with open(dataset_file, "r", encoding="utf-8") as f:
            dataset = json.load(f)

        total = len(dataset)
        score = 0.0
        mrr_total = 0.0
        ndcg_total = 0.0

        for item in dataset:
            query = item["search_string"]
            expected_file = item["expected_result_file"]

            query_vec = get_embedding(query)
            results = index.search(np.array(query_vec), top_k=5)

            found = False
            best_score = results[0]["score"] if results else 0.0

            for rank, hit in enumerate(results):
                result_file = eid_to_text[hit["eid"]]["file"]
                if result_file == expected_file:
                    found = True
                    break

            mrr = compute_mrr(results, expected_file, eid_to_text)
            ndcg = compute_ndcg(results, expected_file, eid_to_text)
            mrr_total += mrr
            ndcg_total += ndcg

            if found:
                s = hit["score"]
                rel = s / best_score if best_score > 0 else 0
                final_score = min(1.0, rel)

                if final_score >= 0.95:
                    marker = "✅"
                elif final_score >= 0.85:
                    marker = "🟡"
                elif final_score >= 0.70:
                    marker = "🟠"
                else:
                    marker = "❌"

                print(f"{marker} Query: '{query}' found '{expected_file}' at rank {rank+1} | score: {final_score:.3f}")
                score += final_score
            else:
                print(f"❌ Query: '{query}' expected '{expected_file}' not in top 5")

        print(f"\n📊 Test set results:")
        print(f" - Accuracy: {score:.2f} / {total:.2f} ({(score / total) * 100:.1f}% effectiveness)")
        print(f" - MRR: {mrr_total / total:.3f}")
        print(f" - NDCG@5: {ndcg_total / total:.3f}")

    if cleanup and not memory_only and not load_existing:
        for eid in saved_eids:
            delete_embedding(eid, silent=True)
        print(f"🧹 Cleanup complete. Removed {len(saved_eids)} embeddings.")

if __name__ == "__main__":
    test_directory_embedding_search(memory_only=False, load_existing=True, cleanup=False)
