import sqlite3
from typing import Optional

class Message:
    def __init__(self, id: int, message: Optional[str], file: Optional[bytes], contact: str, is_self: bool):
        self.id = id
        self.message = message
        self.file = file
        self.contact = contact
        self.is_self = is_self

class Writer:
    def __init__(self):
        self.conn = sqlite3.connect('messages.db')
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.cursor.close()
        self.conn.close()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY NOT NULL,
            message TEXT,
            file BLOB,
            contact TEXT NOT NULL,
            isself BOOLEAN NOT NULL
        )
        """)

    def write(self, message: Optional[str], file: Optional[bytes], contact: str, is_self: bool):
        self.cursor.execute("INSERT INTO messages (message, file, contact, isself) VALUES (?, ?, ?, ?)", (message, file, contact, is_self))
        self.conn.commit()

    def load_from_contact(self, contact: str):
        self.cursor.execute("SELECT * FROM messages WHERE contact = ?", (contact,))
        return [Message(*row) for row in self.cursor.fetchall()]
    
    def load_all(self):
        self.cursor.execute("SELECT * FROM messages")
        return [Message(*row) for row in self.cursor.fetchall()]