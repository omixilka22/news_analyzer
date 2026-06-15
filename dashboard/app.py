import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import matplotlib.pyplot as plt
from db.repository import get_articles_df
from analysis.trends import get_top_words, get_sentiment_stats, get_daily_stats
import seaborn as sns

st.set_page_config(page_title="News Analyzer", layout="wide")

@st.cache_data(ttl=300)
def load_data():
    return get_articles_df()

df = load_data()

# Sidebar
st.sidebar.title("Фільтри")
sentiment_filter = st.sidebar.selectbox(
    "Sentiment",
    ["all", "positive", "negative", "neutral"]
)

st.sidebar.divider()
st.sidebar.markdown("### 🔄 Оновлення даних")

if st.sidebar.button("Оновити новини"):
    from scrapy.scraper import fetch_articles
    from db.repository import insert_article, get_latest_article_date
    from analysis.sentiment import analyze_df, save_sentiments
    from datetime import datetime, timezone

    latest = get_latest_article_date()
    if latest:
        diff = datetime.now(timezone.utc) - latest.replace(tzinfo=timezone.utc)
        if diff.total_seconds() < 3600:
            st.sidebar.warning("Нових новин немає — дані актуальні!")
        else:
            with st.spinner("Збираємо новини..."):
                articles = fetch_articles(since=latest)
                for article in articles:
                    insert_article(article)
            with st.spinner("Аналізуємо sentiment..."):
                df_new = get_articles_df()
                df_new = analyze_df(df_new)
                save_sentiments(df_new)
            st.sidebar.success(f"Додано {len(articles)} нових статей!")
            st.cache_data.clear()
            st.rerun()
    else:
        with st.spinner("Перший збір даних..."):
            articles = fetch_articles()
            for article in articles:
                insert_article(article)
        st.sidebar.success("Дані завантажено!")
        st.cache_data.clear()
        st.rerun()

if df is None or df.empty:
    st.warning("База даних порожня. Натисніть 'Оновити новини' в меню зліва.")
    st.stop()

if sentiment_filter != "all":
    df = df[df["sentiment"] == sentiment_filter]

st.title("📰 News Sentiment Analyzer")
st.subheader("Аналіз новин unian.ua")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Всього статей", len(df))
col2.metric("Негативних", len(df[df["sentiment"] == "negative"]))
col3.metric("Нейтральних", len(df[df["sentiment"] == "neutral"]))
col4.metric("Позитивних", len(df[df["sentiment"] == "positive"]))

st.divider()

st.markdown("### 📋 Статті")
st.dataframe(
    df[["title", "published_at", "sentiment", "content"]],
    use_container_width=True
)

st.divider()

st.markdown("### 📈 Візуалізація")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Розподіл sentiment")
    stats = get_sentiment_stats(df)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=stats.index, y=stats.values, ax=ax)
    ax.set_xlabel("Sentiment")
    ax.set_ylabel("Кількість")
    st.pyplot(fig)

with col2:
    st.markdown("#### Топ слова у заголовках")
    top_words = get_top_words(df)
    words = [item[0] for item in top_words]
    counts = [item[1] for item in top_words]
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=counts, y=words, orient='h', ax=ax)
    ax.set_xlabel("Кількість")
    ax.set_ylabel("Слово")
    st.pyplot(fig)

st.markdown("#### Динаміка по днях")
daily = get_daily_stats(df)
fig, ax = plt.subplots(figsize=(12, 4))
sns.lineplot(data=daily, x='date', y='count', hue='sentiment', ax=ax)
ax.set_xlabel("Дата")
ax.set_ylabel("Кількість статей")
st.pyplot(fig)