import mysql.connector
from contextlib import contextmanager

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="",
            database="beatport_db",
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
