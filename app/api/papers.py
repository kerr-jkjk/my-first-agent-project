import sqlite3

from fastapi import APIRouter, HTTPException
from app.services.paper_service import search_papers

from app import db
from app.models.paper import(
    PaperCreate,
    PaperUpdate,
    PaperResponse,
    PaperSearchRequest,
    PaperSearchResponse,
)

# 接收论文相关 HTTP 请求、调用服务、整理响应

router = APIRouter()

def paper_to_dict(row: tuple) -> dict:
    return {
        "id": row[0],
        "title": row[1],
        "url": row[2],
        "created_at": row[3]
    }

@router.get("/papers")
async def list_papers(
    keyword: str|None = None,
    limit: int = 10
):
    return {
        "keyword": keyword,
        "limit": limit
    }

@router.post(
        "/papers",
        response_model=PaperResponse,
        status_code=201,
)
def create_paper(request: PaperCreate):
    try:
        # 尝试新增论文，成功后获得数据库分配的 ID
        paper_id = db.add_paper(request.title, request.url)

    except sqlite3.IntegrityError as exc:
        # 新增过程中出现“违反数据库约束”的异常时，进入这里

        if exc.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
            # 如果违反的是唯一约束，转换成 HTTP 409 错误
            raise HTTPException(
                status_code=409,
                detail="论文 URL 已存在",
            ) from exc

        # 如果是其他数据库约束错误，重新抛出原异常
        raise

    # 只有新增成功，才会继续执行下面两行
    row = db.get_paper(paper_id)
    return paper_to_dict(row)

@router.post(
        "/papers/search",
        response_model=PaperSearchResponse,
)
async def search_papers_api(request: PaperSearchRequest):
    result = await search_papers(request.query)
    papers = []
    for index, title in enumerate(
        result.items[:request.limit],
        start=1,
    ):
        papers.append(
            {
                "id": index,
                "title": title
            }
        )
        
    return {
        "query": request.query,
        "papers": papers
    }
    
@router.get("/papers/{paper_id}")
def get_paper(paper_id: int):
    row = db.get_paper(paper_id)

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="论文不存在"
        )
    return paper_to_dict(row)       

@router.patch(
    "/papers/{paper_id}",
    response_model=PaperResponse,
)
def update_paper_api(paper_id: int, request: PaperUpdate):
    update = db.update_paper_title(paper_id, request.title)

    if not update:
        raise HTTPException(
            status_code=404,
            detail="论文不存在"
        )

    row = db.get_paper(paper_id)
    return paper_to_dict(row)

@router.delete(
    "/papers/{paper_id}",
)
def delete_paper_api(paper_id: int):
    deleted = db.delete_paper(paper_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="论文不存在",
        )

    return {
        "deleted": True,
        "id": paper_id
    }
