import asyncio
import time

def sync_io(name: str, delay: float) -> str:
    print(f"{name} 开始")
    time.sleep(delay)
    print(f"{name} 完成")
    return f"{name} 的结果"

async def async_io(name: str, delay: float) -> str:
    print(f"{name} 开始")
    # await asyncio.sleep(delay) 

    try:
        await asyncio.sleep(delay)
    except asyncio.CancelledError:
        print(f"{name} 收到取消")
        raise

    print(f"{name} 完成")
    return f"{name} 的结果"


async def limited_io(
        name: str,
        delay: float,
        timeout_seconds: float,
) -> str:
    async with asyncio.timeout(timeout_seconds):
        return await async_io(name, delay)


async def main():
    # begin = time.time()
    # sync_io("A", 2)
    # sync_io("B", 3)
    # end = time.time()
    # print("总耗时：", end - begin)

    # begin = time.time()
    # await async_io("A", 2)
    # await async_io("B", 3)
    # end = time.time()
    # print("总耗时：", end - begin)

    # begin = time.time()
    # task1 = asyncio.create_task(
    #     async_io("A", 2)
    # )
    # task2 = asyncio.create_task(
    #     async_io("B", 3)
    # )
    # await task1
    # await task2
    # end = time.time()
    # print("总耗时：", end - begin)


    # begin = time.time()
    # result = await asyncio.gather(
    #     async_io("A", 2),
    #     async_io("B", 3)
    # )
    # end = time.time()
    # print("总耗时：", end - begin)

    start = time.perf_counter()

    try:
        results = await asyncio.gather(
            async_io("A", 1),
            limited_io("B", 3, 4),
        )
        print(results)
    except TimeoutError:
        print("调用方收到TimeoutError")

    print(f"总耗时: {time.perf_counter() - start:.2f} 秒")




if __name__ == "__main__":
    asyncio.run(main())