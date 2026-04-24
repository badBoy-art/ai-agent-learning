# 五、异步网络请求 (httpx)
# pip install httpx

import httpx
import asyncio


# 1. 同步请求 (阻塞)
def sync_request():
    response = httpx.get("https://httpbin.org/get")
    return response.json()


# 2. 异步请求 (非阻塞)
async def async_request(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()


# 3. 并发请求多个URL
async def fetch_multiple_urls():
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/1"
    ]

    async with httpx.AsyncClient() as client:
        # 并发请求
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)

        for i, response in enumerate(responses):
            print(f"URL {i + 1}: {response.status_code}")


# 4. 带超时的请求
async def request_with_timeout():
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get("https://httpbin.org/delay/5")
            return response.json()
        except httpx.TimeoutException:
            return {"error": "请求超时"}


# 5. 带重试的请求
async def request_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                return response.json()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            await asyncio.sleep(1)


# 运行示例
async def main():
    print("=== 并发请求示例 ===")
    await fetch_multiple_urls()

# asyncio.run(main())
