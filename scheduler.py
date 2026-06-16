import schedule
import time
import logging
from datetime import datetime, timezone
from scrapy.scraper import fetch_articles
from db.repository import insert_article, get_articles_df , get_latest_article_date
from analysis.sentiment import analyze_df, save_sentiments

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_scraper():
    try:
        latest = get_latest_article_date()
        if latest:
            # перевіряємо чи є нові новини (новіші за останню в БД)
            now = datetime.now(timezone.utc)
            diff = now - latest.replace(tzinfo=timezone.utc)
            if diff.total_seconds() < 3600:  # менше години
                logging.info("Нових новин немає — пропускаємо")
                return
        logging.info("Починаємо збір новин...")
        articles = fetch_articles(since=latest)
        for article in articles:
            insert_article(article)
        logging.info(f"Зібрано та збережено {len(articles)} статей")

        # Аналіз sentiment
        logging.info("Аналізуємо sentiment...")
        df = get_articles_df()
        df = analyze_df(df)
        save_sentiments(df)
        logging.info("Sentiment збережено")
    except Exception as e:
        logging.error(f"Помилка під час збору: {e}")

if __name__ == "__main__":
    run_scraper()  # перший запуск одразу

    schedule.every(6).hours.do(run_scraper)

    while True:
        schedule.run_pending()
        time.sleep(60)