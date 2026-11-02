import pytest

from fastapi.testclient import TestClient

from app import db  # 数据库操作
from app.api_server import app

# 声明测试 fixture：测试函数使用 client 参数时，pytest 会自动调用它
# 默认每个测试函数各执行一次，提供独立的测试环境
@pytest.fixture
def client(tmp_path, monkeypatch):
    # 临时将数据库路径改到本次测试的目录，避免修改项目中的数据库
    # 测试结束后，monkeypatch 会自动恢复原来的 DB_PATH
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "papers.db")

    # 在临时数据库中创建表和索引
    db.init_db()

    # 为应用创建测试客户端，无需启动 Uvicorn
    # 退出 with 时会清理客户端资源
    with TestClient(app) as test_client:
        # 将客户端交给测试函数，并暂停在这里
        # 测试结束后恢复执行，再退出 with 完成清理
        yield test_client

def test_create_paper(client):
    response = client.post(
        "/papers",
        json={
            "title": "PepMLM",
            "url": "https://example.com/pepmlm",
            "source": "arxiv:123123",
        }
    )

    assert response.status_code == 201
    paper = response.json()
    paper_id = paper["id"]
    assert paper["title"] == "PepMLM"
    assert paper["created_at"]
    assert paper["source"] == "arxiv:123123"
    assert db.get_paper(paper_id)[1] == "PepMLM"
    

def test_list_papers(client):
    responses = [
        client.post("/papers", json={"title": "PepMLM", "url": "asda", "source": "a"}),
        client.post("/papers", json={"title": "PepMLM2", "url": "ada", "source": "abc"}),
        client.post("/papers", json={"title": "PepMLM3", "url": "da"}),
    ]


    results = client.get("/papers")
    assert results.json()[0]["title"] == "PepMLM"
    assert results.json()[0]["url"] == "asda"
    assert results.json()[0]["source"] == "a"

    assert results.json()[1]["title"] == "PepMLM2"
    assert results.json()[1]["url"] == "ada"
    assert results.json()[1]["source"] == "abc"
    
    assert results.json()[2]["title"] == "PepMLM3"
    assert results.json()[2]["url"] == "da"
    assert results.json()[2]["source"] == "manual"

    paper_id = results.json()[0]["id"]
    response = client.get(f"/papers/{paper_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "PepMLM"
    assert response.json()["source"] == "a"


def test_illeagel_source(client):
    responses = [
        client.post("/papers", json={"title": "PepMLM", "url": "asda", "source": ""}),
        client.post("/papers", json={"title": "PepMLM2", "url": "ada", "source": "  "}),
        client.post("/papers", json={"title": "PepMLM3", "url": "da", "source": None}),
    ]

    for response in responses:
        assert response.status_code == 422

def tets_papers_search(client):
    response = client.post("/papers/search")
    assert response.status_code == 200