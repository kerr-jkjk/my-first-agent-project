import asyncio
import time

async def query_api(delay: float) -> str:
    print('API start')
    await asyncio.sleep(delay)

    print('API end')

    return "API result"

async def main() -> None:
    start = time.perf_counter()

    try:
        async with asyncio.timeout(3):
            result = await query_api(4)

        print(result)

    except TimeoutError:
        print("API 请求超过3秒，已超时")

    elapsed = time.perf_counter() - start

    print("实际耗时：%f", elapsed)

if __name__ == "__main__":
    asyncio.run(main())