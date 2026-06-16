import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from datetime import datetime, timedelta
from scrapy.model import Article
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

WAR_LISTING_URL = "https://www.unian.ua/war"
DATE_FORMATS = ("%H:%M, %d.%m.%Y", "%H:%M, %d.%m.%y")
DEFAULT_LOOKBACK_DAYS = 7


def parse_date(time_raw: str) -> Optional[datetime]:
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(time_raw, fmt)
        except ValueError:
            continue
    return None


def get_listing_entries(url: str) -> List[tuple[str, Optional[datetime]]]:
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "lxml")
    entries = []
    for item in soup.find_all("div", class_="list-thumbs__item"):
        link_el = item.find("a", class_="list-thumbs__image") or item.find("a", class_="list-thumbs__title")
        if not link_el:
            continue
        time_el = item.find("div", class_="list-thumbs__time")
        pub_date = parse_date(time_el.get_text(strip=True)) if time_el else None
        entries.append((link_el.get("href"), pub_date))
    return entries


def collect_article_links(since: Optional[datetime] = None) -> List[str]:
    if since is None:
        since = datetime.now() - timedelta(days=DEFAULT_LOOKBACK_DAYS)

    links: List[str] = []
    seen: set[str] = set()
    page = 1

    while True:
        page_url = WAR_LISTING_URL if page == 1 else f"{WAR_LISTING_URL}?page={page}"
        entries = get_listing_entries(page_url)
        if not entries:
            break

        for url, pub_date in entries:
            if url in seen:
                continue
            seen.add(url)
            if pub_date is None or pub_date > since:
                links.append(url)

        if all(pub_date is not None and pub_date <= since for _, pub_date in entries):
            break

        page += 1
        time.sleep(0.3)

    return links


def parse_article(url: str) -> Optional[Article]:
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "lxml")

    h1 = soup.find("h1")
    if not h1:
        return None
    header = h1.get_text(strip=True)

    time_el = (
        soup.find("div", class_=["article__info-item", "time"])
        or soup.find("div", class_=["publication__info-item", "time"])
    )
    if not time_el:
        print(f"Не знайдено дату: {url}")
        return None

    published_at = parse_date(time_el.get_text(strip=True))
    if published_at is None:
        print(f"Невідомий формат дати: {time_el.get_text(strip=True)!r} ({url})")
        return None

    article_div = (
        soup.find("div", class_="article-text")
        or soup.find("div", class_="publication-text")
    )
    if not article_div:
        print(f"Не знайдено текст статті: {url}")
        return None

    paragraphs = article_div.find_all("p")
    content = " ".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
    if not content:
        print(f"Порожній текст статті: {url}")
        return None

    return Article(
        title=header,
        url=url,
        source="unian.ua",
        published_at=published_at,
        content=content,
    )


def fetch_articles(since: Optional[datetime] = None) -> List[Article]:
    links = collect_article_links(since)
    articles = []
    for link in links:
        article = parse_article(link)
        if article:
            articles.append(article)
        time.sleep(1)
    return articles


if __name__ == "__main__":
    articles = fetch_articles()
    for k, article in enumerate(articles, start=1):
        print(f"№{k}  -   {article}")
        print()
