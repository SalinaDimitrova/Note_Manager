from note_manager.db import get_connection
import sqlite3
from typing import Any, Optional

class NoteService:

    def __init__(self, db_path: Optional[str] = None) -> None:
        if db_path:
            self.conn = sqlite3.connect(db_path)
            self.conn.row_factory = sqlite3.Row
        else:
            self.conn = get_connection()

    def add_note(self, title: str, content: str) -> int:
        if not title:
            raise ValueError("Title cannot be empty")

        cursor = self.conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO notes (title, content) VALUES (?, ?)",
                (title, content)
            )
            self.conn.commit()
            return cursor.lastrowid

        except sqlite3.IntegrityError:
            raise ValueError("A note with this title already exists")

    def list_notes(self) -> list[dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, title, content FROM notes")

        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    def get_note(self, note_id: int) -> Optional[dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, title, content FROM notes WHERE id = ?",
            (note_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    def delete_note(self, note_id: int) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM notes WHERE id = ?",
            (note_id,)
        )

        self.conn.commit()

        return cursor.rowcount

    def close(self):
        self.conn.close()