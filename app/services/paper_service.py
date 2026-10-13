import asyncio
import logging

from app.models.search_result import SearchResult

logger = logging.getLogger(__name__)

async def search_papers(keyword: str,) -> SearchResult:
    logger.info(
        "Seaerching papers for: %s", keyword,
    )

    await asyncio.sleep(1.5)

    logger.info("Paper search completed")

    return SearchResult(
        source="paper",
        keyword=keyword,
        items=[
            f"{keyword} paper 1",
            f"{keyword} paper 2",
        ],
    )