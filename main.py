import requests
import time
import re

HEADERS = {"User-Agent": "Mozilla/5.0"}

# 搜索关键词（GitHub 节点仓库）
KEYWORDS = [
    "clash meta nodes",
    "v2ray free sub",
    "vmess vless trojan",
    "clash 订阅 自动更新",
    "free proxy list",
    "hysteria2 sub",
    "shadowsocks nodes",
    "clash nodes daily update"
]

# 从搜索结果提取仓库
def search_github():
    repos = set()
    for kw in KEYWORDS:
        try:
            url = f"https://api.github.com/search/repositories?q={kw}&per_page=30"
            res = requests.get(url, headers=HEADERS, timeout=10).json()
            for item in res.get("items", []):
                repos.add(item["full_name"])
            time.sleep(1)
        except:
            continue
    return list(repos)

# 从仓库里提取节点订阅链接
def find_sub_links(repo):
    links = []
    try:
        url = f"https://api.github.com/repos/{repo}/contents/"
        files = requests.get(url, headers=HEADERS, timeout=10).json()
        for f in files:
            n = f["name"].lower()
            if any(s in n for s in ["clash", "node", "sub", "v2ray", "vmess", "vless", "trojan", "hy2"]):
                if f["type"] == "file" and f["download_url"]:
                    links.append(f["download_url"])
    except:
        pass
    return links

# 主程序
if __name__ == "__main__":
    all_links = set()

    print("正在搜索 GitHub 仓库...")
    repos = search_github()

    print(f"找到 {len(repos)} 个仓库，正在提取订阅链接...")
    for repo in repos:
        links = find_sub_links(repo)
        for l in links:
            all_links.add(l)

    # 保存
    with open("daily-sources.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(all_links)))

    print(f"完成！共获取 {len(all_links)} 条订阅链接")
