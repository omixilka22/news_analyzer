import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    try:
        conn = psycopg2.connect(
            database=os.getenv("DB_NAME", "news_analyzer"),
            user=os.getenv("DB_USER", "pro"),
            password=os.getenv("DB_PASSWORD", ""),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", 5432),
        )
        return conn
    except OperationalError as e:
        print(f"Помилка підключення до бази даних: {e}")
        return None