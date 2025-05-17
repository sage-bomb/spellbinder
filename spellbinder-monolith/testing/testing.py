import uuid
from util.db import TinyInterface
from util.embedding import (
    get_embedding,
    save_embeddings,
    load_embeddings,
    delete_embedding
)
from util.embed_chunker import embed_text_block

char_db = TinyInterface(db_path="data/characters.json", table_name="characters")


def test_character_crud():
    print("\n🔹 Running: Character DB CRUD Test")

    # Add
    char_db.add({"name": "Sahla", "race": "Ara'net", "magic": True})
    print("Added Sahla:", char_db.get(name="Sahla"))

    # Update
    char_db.update({"magic": False}, name="Sahla")
    print("Updated Sahla:", char_db.get(name="Sahla"))

    # Delete
    char_db.delete(name="Sahla")
    print("Deleted Sahla:", char_db.get(name="Sahla"))


def test_batch_embedding_save_load():
    print("\n🔹 Running: Batch Embedding Save/Load Test")

    texts = ["Hello", "Sahla stands", "The wind speaks"]
    embeds = [get_embedding(t) for t in texts]
    metadata = [{"text": t} for t in texts]

    save_embeddings("example", embeds, metadata)
    print("Saved metadata:", metadata)

    vecs, meta = load_embeddings("example")
    print("Loaded:", meta[0]["text"], vecs[0][:5])

    delete_embedding("example")


def test_single_embedding_uuid():
    print("\n🔹 Running: UUID Embedding + Character Link Test")

    # Step 1: Embed
    text = "Roan survived the blade not by skill, but by mercy."
    vec = get_embedding(text)

    # Step 2: UUID
    eid = str(uuid.uuid4())
    save_embeddings(eid, [vec])  # must wrap in list!

    # Step 3: Link UUID to character record
    char_db.add({
        "name": "Roan",
        "summary_embed_id": eid,
        "origin": "Halewood survivors"
    })

    # Retrieve and use
    result = char_db.get(name="Roan")
    print("Retrieved Roan:", result)

    emb, _ = load_embeddings(eid)
    print("Embedding vector (first 10 dims):", emb[0][:10])

    # Cleanup
    delete_embedding(eid)
    char_db.delete(name="Roan")



def test_embed_chunker():
    text = """
    Sahla stood at the cliff’s edge. The sea below whispered her name.
    Roan was quiet beside her, fists clenched.
    Somewhere behind them, the world burned. But not here. Not now.
    """

    results = embed_text_block(text)
    print(f"Chunks embedded: {len(results)}")
    print("First EID:", results[0]["eid"])
    print("First Vector Sample:", results[0]["embedding"][:5])


if __name__ == "__main__":
    test_character_crud()
    test_batch_embedding_save_load()
    test_single_embedding_uuid()
    test_embed_chunker()
