import asyncio

async def slow_operation() -> str:
    await asyncio.sleep(3)
    return "finish"

async def main() -> None:
    try:
        async with asyncio.timeout(3):
            result = await slow_operation()
        print(result)

    except TimeoutError:
        print("请求超时")

if __name__ == "__main__":
    asyncio.run(main())