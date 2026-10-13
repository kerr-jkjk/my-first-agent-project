import asyncio

async def a():
    return 1


s = asyncio.run(a())

print(s)