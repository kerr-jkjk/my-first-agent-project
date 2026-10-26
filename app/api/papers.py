from fastapi import APIRouter
from fastapi import FastAPI
from app.models.paper import PaperSearchRequest, PaperSearchResponse
from app.services.paper_service import search_papers

router = APIRouter()

app = FastAPI()

@app.get("/health")
async def health():
    return {
        "status": "ok"
    }

@app.get("/")
async def root():
    return {
        "message": "my Agent API"
    }

@app.get("/papers/{paper_id}")
async def get_paper(paper_id: int):
    return {
        "paper_id": paper_id
    }

@app.get("/papers")
async def list_papers(
    keyword: str|None = None,
    limit: int = 10
):
    return {
        "keyword": keyword,
        "limit": limit
    }

@app.post(
        "/papers/search",
        response_model=PaperSearchResponse,
)
async def search_papers_api(
    request: PaperSearchRequest
):
    return {
        "query": request.query,
        "papers": [
            {
                "id": 1,
                "title": "paper 1"
            }
        ],
    }
