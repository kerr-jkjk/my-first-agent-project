import sqlite3
import pytest
from app import db

@pytest.fixture
def isolated_db(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "papers.db")
    db.init_db()

# 全部成功就保存
def test_batch_insert_success(isolated_db):
    paper_ids = db.add_papers_atomic([
        ("Paper A", "https://example.com/a"),
        ("Paper B", "https://example.com/b"),
    ])

    assert len(paper_ids) == 2
    assert db.get_paper(paper_ids[0])[1] == "Paper A"
    assert db.get_paper(paper_ids[1])[1] == "Paper B"

# 同一个事务出现错误，则都不保存，不影响之前的插入结果
def test_batch_insert_rollback(isolated_db):
    existing_url = "https://example.com/existing"

    existing_id = db.add_paper("Existing Paper", existing_url)

    with pytest.raises(sqlite3.IntegrityError):
        db.add_papers_atomic([
            ("Draft Paper", "https://example.com/draft"),
            ("Duplicate Paper", existing_url),
        ])

    assert db.get_paper(existing_id)[1] == "Existing Paper"

    rows = db.list_papers(limit=100)
    assert len(rows) == 1
    assert [row[2] for row in rows] == [existing_url]