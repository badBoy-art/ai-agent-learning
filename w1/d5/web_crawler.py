import asyncio
import aiohttp
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class WebPage:
    url: str
    status_code: int
    title: str
    content: str
    links: List[str] = field(default_factory=list)
    word_count: int = 0
    fetch_time: float = 0.0

    def extract_links(self) -> List[str]:
        # 简单的链接提取
        pattern = r'href=["\'](https?://[^"\']+)["\']'
        return re.findall(pattern, self.content)

    def count_words(self) -> Dict[str, int]:
        # 简单的词频统计
        words = re.findall(r'\b\w+\b', self.content.lower())
        return dict(Counter(words).most_common(20))

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "status_code": self.status_code,
            "title": self.title,
            "word_count": self.word_count,
            "links_count": len(self.links),
            "fetch_time": self.fetch_time
        }


class AsyncWebCrawler:
    def __init__(self, timeout: float = 10.0, max_concurrent: int = 5):
        self.timeout = timeout
        self.max_concurrent = max_concurrent
        self.results: List[WebPage] = []

    async def fetch_page(self, session: aiohttp.ClientSession, url: str) -> Optional[WebPage]:
        start_time = asyncio.get_event_loop().time()

        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=self.timeout)) as response:
                content = await response.text()
                fetch_time = asyncio.get_event_loop().time() - start_time

                # 提取标题
                title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
                title = title_match.group(1) if title_match else "无标题"

                page = WebPage(
                    url=url,
                    status_code=response.status,
                    title=title,
                    content=content,
                    fetch_time=fetch_time
                )

                # 提取链接
                page.links = page.extract_links()
                page.word_count = len(re.findall(r'\b\w+\b', content))

                return page

        except Exception as e:
            print(f"爬取失败 {url}: {e}")
            return None

    async def crawl(self, urls: List[str]) -> List[WebPage]:
        print(f"开始爬取 {len(urls)} 个URL...")

        connector = aiohttp.TCPConnector(limit=self.max_concurrent)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [self.fetch_page(session, url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            self.results = [r for r in results if isinstance(r, WebPage)]
            return self.results

    def get_statistics(self) -> Dict:
        if not self.results:
            return {}

        return {
            "total_pages": len(self.results),
            "success_count": sum(1 for r in self.results if r.status_code == 200),
            "avg_fetch_time": sum(r.fetch_time for r in self.results) / len(self.results),
            "total_words": sum(r.word_count for r in self.results),
            "total_links": sum(len(r.links) for r in self.results)
        }

    def save_results(self, filepath: str) -> None:
        data = {
            "timestamp": datetime.now().isoformat(),
            "statistics": self.get_statistics(),
            "pages": [p.to_dict() for p in self.results]
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"结果保存到: {filepath}")
