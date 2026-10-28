import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "papers.db"

def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db() -> None:
    conn = get_connection()

    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS papers (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_papers_url_unique
            ON papers(url)
        """)
        conn.commit()
    finally:
        conn.close()


def add_paper(title: str, url: str) -> int:
    conn = get_connection()

    try:
        cursor = conn.execute(
            "INSERT INTO papers (title, url) VALUES (?, ?)",
            (title, url),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def list_papers() -> list[tuple]:
    conn = get_connection()

    try:
        cursor = conn.execute("""
            SELECT id, title, url, created_at
            FROM papers
            ORDER BY id
        """)
        return cursor.fetchall()
    finally:
        conn.close()

def get_paper(paper_id: int) -> tuple | None:
    conn = get_connection()

    try:
        cursor = conn.execute("""
            SELECT id, title, url, created_at
            FROM papers
            WHERE id = ?
        """, (paper_id,)
        )
        return cursor.fetchone()
    finally:
        conn.close()

def find_papers_by_title(title: str) -> list[tuple]:
    conn = get_connection()

    try:
        cursor = conn.execute("""
            SELECT id, title, url, created_at
            FROM papers
            WHERE title = ?
            ORDER BY id
        """, (title, ))
        return cursor.fetchall()
    finally:
        conn.close()

def update_paper_title(paper_id: int, title: str) -> bool:
    conn = get_connection()

    try:
        cursor = conn.execute("""
            UPDATE papers
            SET title = ?
            WHERE id = ?
        """, (title, paper_id))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def delete_paper(paper_id: int):
    conn = get_connection()

    try:
        cursor = conn.execute("""
            DELETE FROM papers WHERE id = ?
        """, (paper_id, ))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()