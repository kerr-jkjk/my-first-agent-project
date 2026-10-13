# import asyncio

# async def say_hello() -> None:
#     print("1. 开始")
#     await asyncio.sleep(2)
#     print("2. 结束")

# async def main() -> None:
#     await say_hello()

# if __name__ == "__main__":
#     asyncio.run(main())


import asyncio
import time
import logging

logger = logging.getLogger(__name__)

async def search_paper() -> str:
    print("1. 开始")
    await asyncio.sleep(2)
    print("1. 结束")
    return "paper_result"


async def search_protein() -> str:
    print("2. 开始")
    await asyncio.sleep(3)
    print("2. 结束")
    return "protein_result"

async def search_database() -> str:
    print("3. 开始")
    await asyncio.sleep(4)
    print("3. 结束")
    return "database_result"

# async def main() -> None:
#     start = time.perf_counter()
#     result = await asyncio.gather(
#         search_paper(),
#         search_protein(),
#         search_database(),
#     )
#     elapsed = time.perf_counter() - start
#     print(result)
#     print("耗时：%fs", elapsed)


async def main():
    start = time.perf_counter()
    task_a = asyncio.create_task(search_database())
    task_b = asyncio.create_task(search_protein())
    task_c = asyncio.create_task(search_paper())

    await asyncio.sleep(3)

    a = await task_a
    b = await task_b
    c = await task_c

    elapsed = time.perf_counter() - start

    # logger.info("spend time: %d s", elapsed)
    print(elapsed)


if __name__ == "__main__":
    asyncio.run(main())
