import re
from collections import Counter
import pandas as pd

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s'’]", "", text)
    return text

def get_top_words(df, n=20):
    titles = df["title"].tolist()
    all_words = []
    for title in titles:
        words = clean_text(title).split()
        all_words.extend([w for w in words if len(w) > 3])

    k = Counter(all_words)
    return k.most_common(n)

def get_sentiment_stats(df):
    return df['sentiment'].value_counts()

def get_daily_stats(df):
    df["date"] = pd.to_datetime(df["published_at"]).dt.date
    return df.groupby(["date", "sentiment"]).size().reset_index(name="count")

def get_article_with_negative_sentiment(df):
    return df[df["sentiment"] == "negative"]


