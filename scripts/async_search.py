import asyncio
import json
import time
from dataclasses import asdict

from app.models.search_result import SearchResult
from app.services.async_utils import run_with_timeout
from app.services.database_service import search_database
from app.services.paper_service import search_papers
from app.services.protein_service import search_protein

async def search_all(keyword: str) -> list[SearchResult]:

    result = await asyncio.gather(
        run_with_timeout("paper", keyword, search_papers(keyword)),
        run_with_timeout("protein", keyword, search_protein(keyword)),
        run_with_timeout("database", keyword, search_database(keyword))
    )
    return list(result)

async def main() -> None:
    keyword = input("请输入关键词：").strip()

    if not keyword:
        print("关键词不能为空")
        return

    start = time.perf_counter()

    results = await search_all(keyword)

    elapsed = time.perf_counter() - start

    output = [
        asdict(result)
        for result in results
    ]

    print(
        json.dumps(
            output,
            ensure_ascii=False,
            indent=2
        )
    )

    print(f"\n总耗时：{elapsed:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())