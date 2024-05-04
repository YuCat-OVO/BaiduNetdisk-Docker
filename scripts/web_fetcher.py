import json
import random
import re

import httpx
from lxml import etree


class WebFetcher:
    def __init__(self) -> None:
        uas = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        ]
        self.ua = random.choice(uas)

    def fetcher(self, url: str, max_attempt: int = 5) -> str | None:
        """网址抓取器

        从给定 url 抓取对应数据, 失败时重试, 默认重试5次

        >>> bdnd = WebFetcher()
        >>> type(bdnd.fetcher("https://pan.baidu.com/download")) is str
        True
        >>> type(bdnd.fetcher("https://1.1.1.1", max_attempt=1)) is str
        True
        >>> bdnd.fetcher("https://172.1.1.1", max_attempt=1)
        An error occurred: timed out

        Args:
            url: 网址
            max_attempt: 重试次数

        Returns:
            成功时返回所获取网页的text数据
            失败时返回None
        """
        for _ in range(max_attempt):
            try:
                response = httpx.get(
                    url,
                    headers={
                        "User-Agent": self.ua,
                        "Referer": "https://pan.baidu.com/disk/main",
                    },
                    timeout=10,
                )
                return response.text
            except httpx.HTTPError as e:
                print(f"An error occurred: {e}")

    async def async_fetcher(self, url: str, max_attempt: int = 5) -> str | None:
        for attempt in range(max_attempt):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        url,
                        headers={
                            "User-Agent": self.ua,
                            "Referer": "https://pan.baidu.com/disk/main",
                        },
                        timeout=10,
                    )
                return response
            except httpx.HTTPError as e:
                print(f"An error occurred: {e}")
        print(f"Fetch {0} failed after several attempts", url)
        return None

    def fetch_js_url(self) -> list:
        """请求百度网盘下载页,获取存在下载链接的js文件

        Returns:
            成功时设置self.js_url为所获取网页的text数据
            失败时设置self.js_url为None

        >>> bdnd = WebFetcher()
        >>> bdnd.fetch_js_url()
        'https://nd-static.bdstatic.com/m-static/wp-brand/js/chunk-common.8b953c6c.js'
        """
        response = self.fetcher("https://pan.baidu.com/download")
        if response is not None:
            try:
                doc = etree.HTML(response, parser=None)
                for i in doc.xpath("//script/@src"):
                    if re.search(r"https:\/\/.*chunk-common.*\.js", i):
                        self.js_url = i
                        return i
            except Exception as e:
                print(f"An error occurred: {e}, set js_url to default")
                self.js_url = "https://nd-static.bdstatic.com/m-static/wp-brand/js/chunk-common.8b953c6c.js"
                return self.js_url
        else:
            print("Fetcher return None, set js_url to default")
            self.js_url = "https://nd-static.bdstatic.com/m-static/wp-brand/js/chunk-common.8b953c6c.js"
            return self.js_url

    def parse_url_from_js(self) -> list:
        """从js文件中提取下载的链接并且去重

        >>> bdnd = WebFetcher()
        >>> bdnd.fetch_js_url()
        'https://nd-static.bdstatic.com/m-static/wp-brand/js/chunk-common.8b953c6c.js'
        >>> len(bdnd.parse_url_from_js())
        6
        """
        # 获取js数据
        js_url = self.js_url
        response = self.fetcher(js_url)

        # 过滤链接
        original_url = re.findall(
            r'(?:(?:link|url)(?:_[0-9])?:")(?P<link>https://[a-zA-Z/\.]*?/netdisk/[a-zA-Z10-9/\._-]*?)(?=")',
            response,
        )

        # 去重
        unique_url = []
        for i in original_url:
            if i not in unique_url:
                unique_url.append(i)
        self.link_url = unique_url
        return unique_url

    def json_saver(self):
        try:
            with open("url.json", "w") as f:
                f.write(json.dumps(self.link_url, sort_keys=True, indent=4))
        except Exception as e:
            print(f"An error occurred: {e}, Please check the permissions.")

    def run(self):
        doc = WebFetcher()
        doc.fetch_js_url()
        doc.parse_url_from_js()
        doc.json_saver()
        return self.link_url

    def get_urls(self) -> list:
        return self.link_url


if __name__ == "__main__":
    import doctest

    doctest.testmod()
