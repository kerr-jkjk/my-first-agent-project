import asyncio
from dataclasses import dataclass
from typing import Any

import httpx

REQUEST_TIMEOUT = httpx.Timeout(3.0, connect=1.0)


@dataclass
class HttpResult:
    status_code: int | None = None
    data: dict[str, Any] | None = None
    error: str | None = None


# 输入：一个已创建的异步客户端、请求路径、整体等待预算。
# 成功：返回状态码和 JSON 字典，`error` 为 None。
# 失败：返回明确的 error；如果已收到 HTTP 响应，就同时保留状态码。
async def get_json(
        client: httpx.AsyncClient,
        path: str,
        *,
        total_timeout: float = 5.0,
) -> HttpResult:
    try:
        async with asyncio.timeout(total_timeout):
            response = await client.get(path, timeout=REQUEST_TIMEOUT)
    except TimeoutError:
        return HttpResult(error="total_timeout")
    except httpx.ConnectTimeout:
        return HttpResult(error="connect_timeout")
    except httpx.ReadTimeout:
        return HttpResult(error="read_timeout")
    except httpx.TimeoutException:
        return HttpResult(error="network_timeout")
    except httpx.RequestError:
        return HttpResult(error="request_error")

    code = response.status_code

    if code == 429:
        return HttpResult(status_code=code, error="rate_limited")
    if 500 <= code < 600:
        return HttpResult(status_code=code, error="server_error")
    if not response.is_success:
        return HttpResult(status_code=code, error="http_error")

    try:
        payload = response.json()
    except ValueError:
        return HttpResult(status_code=code, error="invalid_json")

    if not isinstance(payload, dict):
        return HttpResult(status_code=code, error="expected_json_object")

    return HttpResult(status_code=code, data=payload)