import sqlite3
from pathlib import Path
from typing import Optional


class SQLiteSession:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None

    def __enter__(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def __exit__(self, exc_type, exc, tb) -> bool:
        if self.connection is None:
            return False

        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()

        self.connection.close()
        return False
