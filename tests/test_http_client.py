import asyncio

import httpx
import pytest

from app.clients.http import get_json

# 用mock模拟故障
def call_with_mock(handler, *, total_timeout=5.0):
    # handler 是处理模拟请求的函数，由它决定返回什么响应。
    # * 后面的参数只能按名字传，例如 total_timeout=0.1。
    async def run():
        # async with 在退出代码块时自动关闭客户端。
        async with httpx.AsyncClient(
            # 把相对路径 /health 拼成 https://example.test/health。
            base_url="https://example.test",
            # HTTPX 会把请求交给 handler，整个过程不访问网络。
            transport=httpx.MockTransport(handler),
        ) as client:
            # 等待 get_json 处理模拟响应，并把它的结果返回给外层。
            return await get_json(
                client,
                "/health",
                total_timeout=total_timeout,  # 把总超时设置传给 get_json。
            )

    # run() 创建协程，asyncio.run() 执行它并取回结果。
    # 这样普通的 def 测试函数也能调用这段异步代码。
    return asyncio.run(run())


def test_get_json_success():
    def handler(request):
        assert request.method == "GET"
        assert request.url.path == "/health"
        return httpx.Response(200, json={"status": "ok"})

    result = call_with_mock(handler)

    assert result.status_code == 200
    assert result.data == {"status": "ok"}
    assert result.error is None

@pytest.mark.parametrize(
    ("status_code", "expected_error"),
    [(429, "rate_limited"), (503, "server_error")],
)
def test_get_json_http_failure(status_code, expected_error):
    def handler(request):
        return httpx.Response(status_code, text="upstream failure")

    result = call_with_mock(handler)

    assert result.status_code == status_code
    assert result.data is None
    assert result.error == expected_error


@pytest.mark.parametrize(
    ("exception_type", "expected_error"),
    [
        (httpx.ConnectTimeout, "connect_timeout"),
        (httpx.ReadTimeout, "read_timeout"),
    ],
)
def test_get_json_network_timeout(exception_type, expected_error):
    def handler(request):
        raise exception_type("simulated timeout", request=request)

    result = call_with_mock(handler)

    assert result.status_code is None
    assert result.error == expected_error

def test_get_json_total_timeout():
    async def handler(request):
        await asyncio.sleep(10)
        return httpx.Response(200, json={"status": "ok"})

    result = call_with_mock(handler, total_timeout=0.05)

    assert result.status_code is None
    assert result.error == "total_timeout"