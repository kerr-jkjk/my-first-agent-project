import asyncio
import httpx

from app.clients.http import get_json

async def main():
    async with httpx.AsyncClient(
        base_url = "http://127.0.0.1:8005",
        trust_env = False,
    ) as client:
        result = await get_json(client, "/health")
        print(result.status_code)
        print(result)

if __name__ == "__main__":
    asyncio.run(main())