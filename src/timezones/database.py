import tinydb
from pathlib import Path
from typing import List


class TimezoneDatabase:
    def __init__(self, db_path: Path):
        self._db = tinydb.TinyDB(db_path, create_dirs=True)

    def create(self, data: dict) -> int:
        id = self._db.insert(data)
        return id

    def update(self, id, data: dict) -> List[int]:
        updates = {k: v for k, v in data.items() if v is not None}
        return self._db.update(updates, doc_ids=[id])

    def get_timezone(self, city) -> List:
        return self._db.get(tinydb.Query().city == city)

    def get_all(self) -> tinydb.TinyDB:
        return self._db

    def remove(self, id: int) -> List[int]:
        return self._db.remove(doc_ids=[id])

    def remove_all(self) -> None:
        self._db.truncate()

    def count(self) -> int:
        return len(self._db)

    def close(self) -> None:
        self._db.close()
