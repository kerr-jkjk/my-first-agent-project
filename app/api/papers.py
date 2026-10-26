from fastapi import APIRouter
from fastapi import FastAPI
from app.models.paper import PaperSearchRequest, PaperSearchResponse
from app.services.paper_service import search_papers

# 接收论文相关 HTTP 请求、调用服务、整理响应

router = APIRouter()

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
async def get_paper(paper_id: int):
    return {
        "paper_id": paper_id
    }        


