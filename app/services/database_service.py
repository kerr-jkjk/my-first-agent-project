import asyncio
import logging

from app.models.search_result import SearchResult

logger = logging.getLogger(__name__)

async def search_database(keyword: str) -> SearchResult:

    logger.info(
        "Searching database for: %s",
        keyword
    )

    await asyncio.sleep(5.0)

    logger.info("Database search completed")

    return SearchResult(
        source="database",
        keyword=keyword,
        items=[
            f"{keyword} database record 1",
            f"{keyword} database record 2"
        ]
    )