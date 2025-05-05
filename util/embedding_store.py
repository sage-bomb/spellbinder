class EmbeddingStore:
    """
    Memory-only store for temporary embedding workflows.
    Usage:
        store = EmbeddingStore()
        eid = store.save(vec)
        vec = store.load(eid)
    """
    def __init__(self):
        self._store = {}

    def save(self, eid: str, vec):
        self._store[eid] = vec

    def load(self, eid: str):
        return self._store.get(eid)

    def delete(self, eid: str):
        if eid in self._store:
            del self._store[eid]

    def clear(self):
        self._store.clear()

    def all_items(self):
        return self._store.items()
