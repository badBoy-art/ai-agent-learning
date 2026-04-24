# 九、实战: 异步爬虫
import httpx
import asyncio
from dataclasses import dataclass


@dataclass
class Page:
    url: str
    status: int
    title: str
    content_length: int


async def fetch_page(client, url):
    """获取单个页面"""
    try:
        response = await client.get(url)

        # 简单提取标题
        content = response.text
        title_start = content.find("<title>")
        title_end = content.find("</title>")
        title = content[title_start + 7:title_end] if title_start != -1 else "无标题"

        return Page(
            url=url,
            status=response.status_code,
            title=title,
            content_length=len(content)
        )
    except Exception as e:
        return Page(url=url, status=0, title=f"错误: {e}", content_length=0)


async def crawl_urls(urls):
    """并发爬取多个URL"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [fetch_page(client, url) for url in urls]
        pages = await asyncio.gather(*tasks)
        return pages


# 使用示例
async def main():
    urls = [
        "https://httpbin.org",
        "https://example.com",
        "https://httpbin.org/get"
    ]

    print("开始爬取...")
    pages = await crawl_urls(urls)

    print("\n爬取结果:")
    for page in pages:
        print(f"  URL: {page.url}")
        print(f"  状态: {page.status}")
        print(f"  标题: {page.title}")
        print(f"  长度: {page.content_length}")
        print()


asyncio.run(main())
