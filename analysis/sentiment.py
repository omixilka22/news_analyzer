from transformers import pipeline
import pandas as pd
from db.connection import get_connection
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

def load_model():
    model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
    sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)
    return sentiment_task

def analyze_text(pipe, text):
    if text is None:
        return None
    truncated = text[:512]
    result = pipe(truncated)
    return result[0]

def analyze_df(df):
    pipe = load_model()
    sentiments = []
    for index, row in df.iterrows():
        sentiment = analyze_text(pipe, row['content'])
        sentiments.append(sentiment["label"] if sentiment else None)

    df["sentiment"] = sentiments
    return df

def save_sentiments(df):
    conn = get_connection()

    if conn is None: return None

    try:
        cursor = conn.cursor()
        for index, row in df.iterrows():
            cursor.execute(
                "UPDATE articles SET sentiment = %s WHERE url = %s",
                (row["sentiment"], row["url"])
            )
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
        return None
    finally:
        conn.close()