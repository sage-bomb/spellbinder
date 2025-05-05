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


def test_chapter_embedding_search(memory_only: bool = False):
    # Step 1: Load chapter text
    chapter_path = "testing/test_chapter.txt"
    assert os.path.exists(chapter_path), "Missing test_chapter.txt"
    with open(chapter_path, "r", encoding="utf-8") as f:
        chapter_text = f.read()

    # Step 2: Chunk and embed
    chunks = embed_text_block(chapter_text)

    # Step 3: Setup
    eid_to_text = {}
    saved_eids = []
    index = VectorSearchIndex()
    store = EmbeddingStore() if memory_only else None

    # Step 4: Store embeddings
    for chunk in chunks:
        eid = chunk["eid"]
        vec = np.array(chunk["embedding"], dtype=np.float32)

        if vec.ndim != 1:
            print(f"⚠️ Skipping malformed embedding for eid={eid}: shape={vec.shape}")
            continue

        eid_to_text[eid] = chunk["text"]
        saved_eids.append(eid)

        if memory_only:
            store.save(eid, vec)
            index.add_one(eid, vec)
        else:
            save_embedding(eid, vec)

    print(f"✅ {'Stored in memory' if memory_only else 'Embedded and saved'} {len(eid_to_text)} segments.")

    # Step 5: Build index (disk-based load if not in memory)
    if not memory_only:
        index.add_many([
            {"eid": eid, "embedding": load_embedding(eid)}
            for eid in eid_to_text
        ])

    # Step 6: Run a test query
    query_text = "She stared at the sea, thinking of what was lost."
    query_vec = get_embedding(query_text)
    results = index.search(np.array(query_vec), top_k=5)

    # Step 7: Display results
    print(f"\n🔍 Query: {query_text}\n")
    for r in results:
        print(f"Score: {r['score']:.4f} | EID: {r['eid']}")
        print(f"Text: {eid_to_text[r['eid']]}")
        print("-" * 60)

    # Step 8: Clean up if using disk
    if not memory_only:
        for eid in saved_eids:
            delete_embedding(eid, silent=True)
        print(f"🧹 Cleanup complete. Removed {len(saved_eids)} embeddings.")


if __name__ == "__main__":
    test_chapter_embedding_search(memory_only=True)  # ← flip this for memory mode
