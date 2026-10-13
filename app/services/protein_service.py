import asyncio
import logging

from app.models.search_result import SearchResult

logger = logging.getLogger(__name__)

async def search_protein(keyword: str) -> SearchResult:
    logger.info(
        "Searching proteins for: %s",
        keyword,
    )

    await asyncio.sleep(2.0)

    logger.info("Protein search completed")

    return SearchResult(
        source="protein",
        keyword=keyword,
        items=[
            f"{keyword} protein 1",
            f"{keyword} protein 2",
        ]
    )