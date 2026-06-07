from scrapy.scraper import fetch_articles
from db.repository import insert_article, get_articles_df
from analysis.sentiment import analyze_df, save_sentiments
from analysis.trends import get_top_words, get_sentiment_stats, get_daily_stats , get_article_with_negative_sentiment
from analysis.visualize import plot_sentiment_distribution, plot_top_words, plot_daily_stats


if __name__ == "__main__":

    # articles = fetch_articles()
    # print(f"Знайдено статей: {len(articles)}")
    #
    # for article in articles:
    #     insert_article(article)
    # print("Збережено в БД")

    df = get_articles_df()
    # print(df.head())
    #
    # df = analyze_df(df)
    # print(df[["title", "sentiment"]])

    # save_sentiments(df)

    # print(get_top_words(df))
    # print(get_sentiment_stats(df))
    # print(get_daily_stats(df))
    # print(get_article_with_negative_sentiment(df))

    plot_sentiment_distribution(df)
    plot_top_words(df)
    plot_daily_stats(df)