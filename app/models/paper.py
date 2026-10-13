from pydantic import BaseModel

class PaperSearchRequest(BaseModel):
    query: str
    limit: int = 5

class PaperItem(BaseModel):
    id: int
    title: str

class PaperSearchResponse(BaseModel):
    query: str
    papers: list[PaperItem]