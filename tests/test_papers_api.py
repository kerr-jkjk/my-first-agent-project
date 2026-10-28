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


def test_papers_crud(client):
    # 这里的 client，就是上面 yield 出来的 test_client
    # 新增
    response = client.post(
        "/papers",
        json={
            "title": "PepMLM",
            "url": "https://example.com/pepmlm",
        },
    )

    assert response.status_code == 201

    paper = response.json()
    paper_id = paper["id"]
    assert paper["title"] == "PepMLM"
    assert paper["created_at"]
    assert db.get_paper(paper_id)[1] == "PepMLM"

    # 查询
    response = client.get(f"/papers/{paper_id}")
    assert response.status_code == 200
    assert response.json()["url"] == "https://example.com/pepmlm"

    # 更新
    response = client.patch(
        f"/papers/{paper_id}",
        json={"title": "PepMLM Update"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "PepMLM Update"
    assert db.get_paper(paper_id)[1] == "PepMLM Update"

    # 删除
    response = client.delete(f"/papers/{paper_id}")
    assert response.status_code == 200
    assert response.json()["deleted"] is True
    assert db.get_paper(paper_id) is None

    # 删除后再次查询
    response = client.get(f"/papers/{paper_id}")
    assert response.status_code == 404

"""
    测试不存在的记录
"""
def test_paper_not_found(client):
    responses = [
        client.get("/papers/999"),
        client.patch("/papers/999", json={"title": "Update"}),
        client.delete("/papers/999")
    ]

    for response in responses:
        assert response.status_code == 404
        assert response.json()["detail"] == "论文不存在"

"""
    测试重复URL
"""
def test_duplicate_paper_url(client):
    payload = {
        "title": "PepMLM",
        "url": "https://example.com/pepmlm",
    }

    first = client.post("/papers", json=payload)
    second = client.post("/papers", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409
    assert second.json()["detail"] == "论文 URL 已存在"
    assert len(db.list_papers()) == 1


"""
    测试非法字段
"""
def test_invalid_paper_fields(client):
    payloads = [
        {"title": "", "url": "https://example.com/a"},
        {"title": "Paper", "url": ""},
        {"title": "Paper"},
    ]

    for payload in payloads:
        response = client.post("/papers", json=payload)
        assert response.status_code == 422

    assert db.list_papers() == []

