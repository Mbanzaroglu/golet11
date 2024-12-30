import mysql.connector
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()


def connect_db():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            port=os.getenv('MYSQL_PORT'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_USER_PASSWORD'),
            database=os.getenv('MYSQL_DB'),
            ssl_disabled=True 
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Veritabanı bağlantı hatası: {err}")
        return None

@contextmanager
def get_db_connection_and_cursor():
    conn = connect_db()
    if conn is None:
        raise Exception("Veritabanı bağlantısı kurulamadı.")
    cursor = conn.cursor(dictionary=True)
    try:
        yield conn,cursor
    finally:
        cursor.close()
        conn.close()
