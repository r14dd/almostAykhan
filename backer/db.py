import sqlite3
from pathlib import Path
from backer.config import *


def connection():
    """
    Input: ()
    Output: sqlite connection to the local database file
    """

    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    
    return sqlite3.connect(DB_PATH)


def initialize():

    conn = connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS qa_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            sources TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()
