from scrapy.scraper import fetch_articles
from db.repository import insert_article, get_articles_df

if __name__ == "__main__":

    articles = fetch_articles()
    print(f"Знайдено статей: {len(articles)}")

    for article in articles:
        insert_article(article)
    print("Збережено в БД")

    df = get_articles_df()
    print(df.head())