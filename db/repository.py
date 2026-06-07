from scrapy.scraper import Article
from db.connection import get_connection
import pandas as pd

def insert_article(article: Article):
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        insert_query = ("INSERT INTO articles (title, url , source, published_at, content) "
                        "VALUES (%s, %s ,%s, %s, %s) "
                        "ON CONFLICT (url) DO NOTHING")
        cursor.execute(insert_query, (
            article.title,
            article.url,
            article.source,
            article.published_at,
            article.content
        ))
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Помилка запису: {e}")
        conn.rollback()
    finally:
        conn.close()

def get_articles_df():
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return pd.DataFrame(rows, columns=columns)
    except Exception as e:
        print(e)
        return None
    finally:
        conn.close()

def get_latest_article_date():
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(published_at) FROM articles")
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(e)
        return None
    finally:
        conn.close()