CREATE TABLE IF NOT EXISTS papers (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )

cursor = conn.execute(
            "INSERT INTO papers (title, url) VALUES (?, ?)",
            (title, url),
        )

cursor = conn.execute("""
            SELECT id, title, url, created_at
            FROM papers
            ORDER BY id
        """)

cursor = conn.execute("""
            SELECT id, title, url, created_at
            FROM papers
            WHERE id = ?
        """, (paper_id,))

cursor = conn.execute("""
            SELECT id, title, url, created_at
            FROM papers
            WHERE title = ?
            ORDER BY id
        """, (title, ))

cursor = conn.execute("""
            UPDATE papers
            SET title = ?
            WHERE id = ?
        """, (title, paper_id))

def select(id: int) -> tuple | None:
    conn = get_connection()
    try:
        cursor = conn.execute("""

        """, (,))
        return cursor.fetchone()
    finally:
        conn.close()