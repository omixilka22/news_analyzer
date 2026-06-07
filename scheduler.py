import schedule
import time
import logging
from scrapy.scraper import fetch_articles
from db.repository import insert_article

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_scraper():
    logging.info("Починаємо збір новин...")
    try:
        articles = fetch_articles(limit=50)
        for article in articles:
            insert_article(article)
        logging.info(f"Зібрано та збережено {len(articles)} статей")
    except Exception as e:
        logging.error(f"Помилка під час збору: {e}")

if __name__ == "__main__":
    run_scraper()  # перший запуск одразу

    schedule.every(6).hours.do(run_scraper)

    while True:
        schedule.run_pending()
        time.sleep(60)