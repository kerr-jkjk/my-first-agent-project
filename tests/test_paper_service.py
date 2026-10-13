import asyncio

from app.services.paper_service import search_papers

def test_search_papers():
    result = asyncio.run(search_papers("pepmlm"))

    assert result.keyword == "pepmlm"
    assert result.source == "paper"
    assert result.items == [
        "pepmlm paper 1",
        "pepmlm paper 2",
    ]
    assert result.error is None
