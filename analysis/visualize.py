import matplotlib.pyplot as plt
import seaborn as sns
from analysis.trends import get_top_words, get_sentiment_stats, get_daily_stats , get_article_with_negative_sentiment

def plot_sentiment_distribution(df):
    stats = get_sentiment_stats(df)
    plt.figure(figsize=(8, 5))
    sns.barplot(x=stats.index, y=stats.values)  # index = назви, values = числа
    plt.title("Sentiment Distribution")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.show()

def plot_top_words(df):
    top_words = get_top_words(df)
    words = [item[0] for item in top_words]
    counts = [item[1] for item in top_words]
    plt.figure(figsize=(8, 5))
    sns.barplot(x=counts, y=words , orient='h')
    plt.title("Top Words")
    plt.xlabel("Words")
    plt.ylabel("Count")
    plt.show()

def plot_daily_stats(df):
    stats = get_daily_stats(df)
    sns.lineplot(data=stats, x='date', y='count', hue='sentiment')
    plt.title("Daily Stats")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.show()