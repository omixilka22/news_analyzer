import psycopg2
from psycopg2 import OperationalError

DB_NAME="news_analyzer"
DB_USER="pro"
DB_HOST="localhost"
DB_PORT=5432

def get_connection() :
    try:
        conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password="",
            host=DB_HOST,
            port=DB_PORT,
        )
        return conn
    except OperationalError as e:
        print(f"Помилка підключення до бази даних: {e}")
    return None