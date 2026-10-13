
import asyncio
import logging
from collections.abc import Awaitable

from app.models.search_result import SearchResult


logger = logging.getLogger(__name__)


async def run_with_timeout(
        source: str,
        keyword: str,
        operation: Awaitable[SearchResult],
        timeout_seconds: float = 3.0,
) -> SearchResult:
    try:
        async with asyncio.timeout(timeout_seconds):
            return await operation

    except TimeoutError:
        logger.warning(
            "%s search timed out after $.1f seconds",
            source,
            timeout_seconds,
        )

        return SearchResult(
            source=source,
            keyword=keyword,
            items=[],
            error="timeout"
        )
    