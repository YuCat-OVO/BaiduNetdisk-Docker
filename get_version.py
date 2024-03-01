import json
import re
import time

import requests
from lxml import etree

GLOBAL_HEADER = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

# 截至2024-03-01最新的版本
GLOBAL_VERSION = [
    "https://issuepcdn.baidupcs.com/issue/netdisk/LinuxGuanjia/4.11.5/baidunetdisk-4.11.5.x86_64.rpm",
    "https://issuepcdn.baidupcs.com/issue/netdisk/LinuxGuanjia/4.11.5/baidunetdisk_4.11.5_amd64.deb",
]

# 定义需要检测的版本号范围
max_version = [4, 18, 0]
min_version = [4, 17, 0]

# 定义请求延时时间（秒）
GLOBAL_REQUEST_DELAY = 0.5


def get_js_url() -> str:
    """请求百度网盘下载页,获取存在下载链接的js文件"""
    max_attempts = 5
    attempt = 0

    url = ""
    while attempt < max_attempts:
        try:
            r = requests.get(
                "https://pan.baidu.com/download",
                headers=GLOBAL_HEADER,
            )
            e = etree.HTML(r.text, parser=None)

            # 获取包含链接的js文件
            for i in e.xpath("//script/@src"):
                if re.search("https:\\/\\/.*chunk-common.*\\.js", i):
                    url = i
            # print(url)
            return url
        except Exception as e:
            print(f"An error occurred: {e}")
            attempt += 1
            time.sleep(1)  # 等待1秒再重试

    if attempt == max_attempts:
        print("Failed after several attempts")
    return url


def append_json(json_file_name: str, add):
    """为Json添加并且去重"""
    file = None
    try:
        with open(json_file_name, "r") as f:
            file = json.load(f)
        # print("file=", file)

        u_file = []
        for i in file:
            if i not in u_file:
                u_file.append(i)

    except FileNotFoundError:
        file = json.loads("[]")

    u_file.append(add)

    # print("ufile=", u_file)

    with open(json_file_name, "w") as f:
        f.write(json.dumps(u_file, sort_keys=True, indent=4))
    return


def parse_url_from_json() -> list:
    l = ""
    try:
        with open("url.json", "r") as f:
            l = json.load(f)
    except FileNotFoundError:
        l = []
    return l


def parse_url_from_js():
    """从js文件中提取下载的链接并且去重,写入文件"""
    url = get_js_url()
    u_url = []

    max_attempts = 5
    attempt = 0

    while attempt < max_attempts:
        try:

            d_url = ""
            r = requests.get(
                url,
                headers=GLOBAL_HEADER,
            )
            # 过滤链接
            d_url = re.findall(
                '(?:link|url(?:_[0-9])?):"https://[a-zA-Z/\\.]*?/netdisk/[a-zA-Z10-9/\\._-]*?(?=")',
                r.text,
            )

            # 清理
            for i in range(len(d_url)):
                d_url[i] = re.sub('(link|url(?:_[0-9])?):"', "", d_url[i])

            # 去重
            for i in d_url:
                if i not in u_url:
                    u_url.append(i)

            break
        except Exception as e:
            print(f"An error occurred: {e}")
            attempt += 1
            time.sleep(1)  # 等待1秒再重试

    if attempt == max_attempts:
        print("Failed after several attempts,set url to default")
        u_url = GLOBAL_VERSION

    with open("url.json", "w") as f:
        f.write(json.dumps(u_url, sort_keys=True, indent=4))
    return


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


def make_url_temple():
    l = ""
    url_temple = ""
    try:
        with open("url.json", "r") as f:
            l = json.load(f)
        for i in l:
            if re.search("amd64", i) != None and re.search("deb", i) != None:
                url_temple = re.sub("amd64", "arm64", i)
                url_temple = re.sub(
                    "(?<=[_/])((?:[0-9]{1,2}(?:\\.)?){1,3})(?=[_/])", "{0}", url_temple
                )
                break
        # print(url_temple)
    except FileNotFoundError:
        url_temple = "https://issuepcdn.baidupcs.com/issue/netdisk/LinuxGuanjia/{0}/baidunetdisk_{0}_arm64.deb"
    # print(url_temple)
    return url_temple


def check_version(version):
    """检测指定版本号是否可用"""
    url = make_url_temple().format(".".join(str(v) for v in version))
    # url = "https://httpbin.org/status/200"
    # print("Getting {0}".format(url))

    max_attempts = 5
    attempt = 0

    while attempt < max_attempts:
        try:
            response = requests.head(
                url,
                headers=GLOBAL_HEADER,
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


def find_latest_version(min_version, max_version):
    """寻找最新版本号"""
    version_list = [
        [x, y, z]
        for x in range(max_version[0], min_version[0] - 1, -1)
        for y in range(max_version[1], min_version[1] - 1, -1)
        for z in range(20, -1, -1)
        if not (x == max_version[0] and y == max_version[1] and z > max_version[2])
        if not (x == min_version[0] and y == min_version[1] and z < min_version[2])
    ]
    for version in version_list:
        # 检测指定版本号是否可用
        if check_version(version):
            print("version {0} is available".format(".".join(str(v) for v in version)))
            time.sleep(GLOBAL_REQUEST_DELAY)
            append_json(
                "url.json",
                make_url_temple().format(".".join(str(v) for v in version)),
            )
            return version
        else:
            # print(
            #     "version {0} is not available".format(".".join(str(v) for v in version))
            # )
            time.sleep(GLOBAL_REQUEST_DELAY)

    # 找不到可用版本号，返回None
    return None


if __name__ == "__main__":
    parse_url_from_js()
    find_latest_version(min_version, max_version)
    urls = parse_url_from_json()
    make_info_json(urls)
