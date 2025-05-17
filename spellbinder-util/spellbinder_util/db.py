import os
from tinydb import TinyDB, Query
from typing import Callable, Any



class TinyInterface:
    def __init__(self, db_path=None, table_name="default", validator: Callable[[dict], bool] = None):
        # Always resolve db path relative to project root + data folder
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
        os.makedirs(base_dir, exist_ok=True)
        if db_path is None:
            db_path = os.path.join(base_dir, "db.json")

        self._ensure_path_exists(db_path)
        self.db = TinyDB(db_path)

        self._ensure_path_exists(db_path)
        self.db = TinyDB(db_path)
        self.table = self.db.table(table_name)
        self.validator = validator
    def _ensure_path_exists(self, db_path):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        if not os.path.exists(db_path):
            with open(db_path, 'w') as f:
                f.write("{}")

    def add(self, item: dict) -> int:
        if self.validator and not self.validator(item):
            raise ValueError("Item failed validation.")
        return self.table.insert(item)

    def get(self, **filters) -> list[dict]:
        q = Query()
        query = None
        for key, value in filters.items():
            cond = (q[key] == value)
            query = cond if query is None else query & cond
        return self.table.search(query) if query else []

    def update(self, fields: dict, **filters):
        q = Query()
        query = None
        for key, value in filters.items():
            cond = (q[key] == value)
            query = cond if query is None else query & cond
        return self.table.update(fields, query)

    def delete(self, **filters):
        q = Query()
        query = None
        for key, value in filters.items():
            cond = (q[key] == value)
            query = cond if query is None else query & cond
        return self.table.remove(query)

    def all(self):
        return self.table.all()

    def clear(self):
        self.table.truncate()
