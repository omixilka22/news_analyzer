import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import matplotlib.pyplot as plt
from db.repository import get_articles_df
from analysis.trends import get_top_words, get_sentiment_stats, get_daily_stats
import seaborn as sns

st.set_page_config(page_title="News Analyzer", layout="wide")

@st.cache_data
def load_data():
    return get_articles_df()

df = load_data()

st.title("📰 News Sentiment Analyzer")
st.subheader("Аналіз новин unian.ua")

# Sidebar
st.sidebar.title("Фільтри")
sentiment_filter = st.sidebar.selectbox(
    "Sentiment",
    ["all", "positive", "negative", "neutral"]
)

if sentiment_filter != "all":
    df = df[df["sentiment"] == sentiment_filter]

# Метрики
st.markdown("📊 Загальна статистика")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Всього статей", len(df))
col2.metric("Негативних", len(df[df["sentiment"] == "negative"]))
col3.metric("Нейтральних", len(df[df["sentiment"] == "neutral"]))
col4.metric("Позитивних", len(df[df["sentiment"] == "positive"]))

st.divider()

# Таблиця
st.markdown("### 📋 Статті")
st.dataframe(
    df[["title", "published_at", "sentiment", "content"]],
    use_container_width=True
)

st.divider()

# Графіки
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