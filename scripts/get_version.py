import json
import re
import time

import requests


class LinkObj:
    def __init__(self, link: str) -> None:
        self.link = link
        self.version, self.pkg = re.search(
            r"(?P<version>([0-9]{1,2}(\.)?){3,4}(?=[\._/])).*(?P<pkg>(?<=\.)[a-z]{3,4}$)",
            link,
        ).group("version", "pkg")
        arch = re.search(
            r"(?P<arch>amd64|arm64)",
            link,
        )
        if arch:
            self.arch = arch.group("arch")
        else:
            self.arch = "amd64"


class Version:
    def __init__(self, version, arch_links):
        self.version = version
        self.arch_links = arch_links

    def to_dict(self):
        return self.arch_links.copy()


class Platform:
    def __init__(self) -> None:
        pass


def append_json(json_file_name: str, add):
    """为Json添加元素"""
    file = None
    try:
        with open(json_file_name, "r") as f:
            file = json.load(f)
        # print("file=", file)

    except FileNotFoundError:
        file = json.loads("")

    file.append(add)

    # print("ufile=", u_file)

    with open(json_file_name, "w") as f:
        f.write(json.dumps(file, sort_keys=True, indent=4))
    return


def parse_url_from_json() -> list:
    link = ""
    try:
        with open("url.json", "r") as f:
            link = json.load(f)
    except FileNotFoundError:
        link = []
    return link


def make_info_json(urls: list):
    """保存为Json文件"""
    # print("urls:", urls)
    l_url = urls[-3:]
    # print(l_url)
    j = []
    for i in l_url:
        j.append(
            {
                "version": re.findall("(?<=/)((?:[0-9]{1,2}(?:\\.)?){1,3})(?=/)", i)[0],
                "arch": re.findall("(amd64|arm64|x86_64)", i)[0],
                "pak": re.findall("(rpm|deb)", i)[0],
                "url": i,
            },
        )
    # print(j)
    with open("info.json", "w") as f:
        f.write(json.dumps(j, sort_keys=True, indent=4))
    return


def make_url_temple(arch: str):
    """按照之前所获取的 url.json,创建模板"""
    link = ""
    url_temple = ""
    try:
        with open("url.json", "r") as f:
            link = json.load(f)
        for i in link:
            if re.search("amd64", i) is not None and re.search("deb", i) is not None:
                url_temple = re.sub("amd64", arch, i)
                url_temple = re.sub(
                    "(?<=[_/])((?:[0-9]{1,2}(?:\\.)?){1,3})(?=[_/])", "{0}", url_temple
                )
                break
        # print(url_temple)
    except FileNotFoundError:
        url_temple = "https://issuepcdn.baidupcs.com/issue/netdisk/LinuxGuanjia/{0}/baidunetdisk_{0}_arm64.deb"
    # print(url_temple)
    return url_temple


def check_version(version: list, arch: str):
    """检测指定版本号是否可用"""
    url = make_url_temple(arch).format(".".join(str(v) for v in version))
    # url = "https://httpbin.org/status/200"
    # print("Getting {0}".format(url))

    max_attempts = 5
    attempt = 0

    while attempt < max_attempts:
        try:
            response = requests.head(
                url,
                headers="",
            )
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            print(f"An error occurred: {e}")
            attempt += 1
            time.sleep(1)  # 等待1秒再重试

    if attempt == max_attempts:
        print("Failed after several attempts")

    return


def main():
    pass


if __name__ == "__main__":
    main()
