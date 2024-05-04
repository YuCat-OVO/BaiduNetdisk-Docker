import asyncio
import json
import random
import re

import httpx


class APIFetcher:
    def __init__(self) -> None:
        uas = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        ]
        self.ua = random.choice(uas)

    async def async_fetcher(self, platform: str, max_attempt: int = 5) -> str | None:
        url = "https://yun.baidu.com/disk/cmsdata?platform={0}&page=1&num=100".format(
            platform
        )
        for _ in range(max_attempt):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        url,
                        headers={
                            "User-Agent": self.ua,
                            "Referer": "https://yun.baidu.com/disk/version?errmsg=Auth+Login+Sucess&errno=0&ssnerror=0&",
                        },
                        timeout=10,
                    )
                return response.text
            except httpx.HTTPError as e:
                print(f"An error occurred: {e}")
        print(f"Fetch {0} failed after several attempts", url)
        return None

    def linux_version(self):
        doc = self.linux_json
        version = json.loads(doc)["list"][0]["version"]
        version = re.search(r"(?P<version>([0-9]{1,2}(\.)?){3,4})", version).group(
            "version"
        )

        return version

    def windows_version(self):
        doc = self.windows_json
        version = json.loads(doc)["list"][0]["version"]
        version = re.search(r"(?P<version>([0-9]{1,2}(\.)?){3,4})", version).group(
            "version"
        )
        return version

    def mac_version(self):
        doc = self.mac_json
        version = json.loads(doc)["list"][0]["version"]
        version = re.search(r"(?P<version>([0-9]{1,2}(\.)?){3,4})", version).group(
            "version"
        )
        return version

    async def run(self):
        L = await asyncio.gather(
            self.async_fetcher("linux"),
            self.async_fetcher("windows"),
            self.async_fetcher("mac"),
        )
        # print(L)
        self.linux_json, self.windows_json, self.mac_json = L
        print(self.linux_json)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    af = APIFetcher()
    af.run()
