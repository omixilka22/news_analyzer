import requests
from bs4 import BeautifulSoup
from typing import List, Optional
import lxml
from datetime import datetime
from scrapy.model import Article
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

def get_article_links(url) -> List[str]:
    response = requests.get(url , headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        thumbs = soup.find_all("div" , class_= "list-thumbs__item")
        links = []
        for item in thumbs:
            a = item.find("a", class_="list-thumbs__image")
            if a:
                links.append(a.get("href"))
        return links
    return []

def parse_article(url) -> Optional[Article]:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        header = soup.find("h1").text
        time_raw = soup.find("div", class_=["article__info-item", "time"]).text.strip()
        published_at = datetime.strptime(time_raw, "%H:%M, %d.%m.%y")
        article_div = soup.find("div", class_="article-text")
        paragraphs = article_div.find_all("p")
        content = " ".join([p.text.strip() for p in paragraphs])
        return Article(
            title=header,
            url=url,
            source="unian.ua",
            published_at=published_at,
            content=content,
        )
    return None

def fetch_articles(limit=20) -> List[Article]:
    links = get_article_links("https://www.unian.ua/war")
    articles = []
    for link in links[:limit]:
        article = parse_article(link)
        if article:
            articles.append(article)
        time.sleep(1)
    return articles


if __name__ == "__main__":
    articles = fetch_articles()
    k = 1
    for article in articles:
        print(f"№{k}  -   " , article)
        print()
        k += 1
