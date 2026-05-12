import requests
from bs4 import BeautifulSoup

def get_ptt():
    url = "https://www.ptt.cc/bbs/Gossiping/index.html"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    cookies = {
        "over18": "1"
    }

    res = requests.get(url, headers=headers, cookies=cookies)

    soup = BeautifulSoup(res.text, "html.parser")

    data = []

    for item in soup.select(".r-ent"):
        title = item.select_one(".title").text.strip()
        link = item.select_one("a")
        push = item.select_one(".nrec").text.strip()

        if "爆" in push:
            data.append({
                "title": title,
                "link": "https://www.ptt.cc" + link["href"] if link else "",
                "push": push
            })

    return data