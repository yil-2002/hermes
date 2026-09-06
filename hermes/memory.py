import sqlite3
import threading
from datetime import datetime, timezone

class MemoryStore:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.local = threading.local()
        self._init_db()

    def _get_conn(self):
        if not hasattr(self.local, "conn"):
            self.local.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.local.conn.execute("PRAGMA journal_mode=WAL")
        return self.local.conn

    def _init_db(self):
        conn = self._get_conn()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS spend_ledger (
                date TEXT PRIMARY KEY,
                tokens_in INTEGER,
                tokens_out INTEGER
            )
        """)
        conn.commit()

    def add_spend(self, tokens_in: int, tokens_out: int):
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        conn = self._get_conn()
        conn.execute("""
            INSERT INTO spend_ledger (date, tokens_in, tokens_out)
            VALUES (?, ?, ?)
            ON CONFLICT(date) DO UPDATE SET 
            tokens_in = tokens_in + excluded.tokens_in,
            tokens_out = tokens_out + excluded.tokens_out
        """, (today, tokens_in, tokens_out))
        conn.commit()

    def get_today_spend(self) -> int:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        row = self._get_conn().execute(
            "SELECT tokens_in + tokens_out FROM spend_ledger WHERE date = ?", (today,)
        ).fetchone()
        return row[0] if row else 0
