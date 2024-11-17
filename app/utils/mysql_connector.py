import mysql.connector
from mysql.connector import Error
import pymysql
import os
# Veritabanı bağlantısı
def initialize_database():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="Banzaroglu196761",
        database="bp_database",
        ssl_disabled=True  # SSL'i devre dışı bırak
        )

    def table_exists(table_name):
        #Tablonun veritabaninda mevcut olup olmadığını kontrol eder.
        cursor = conn.cursor()
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def execute_sql_file(file_path):
        # """SQL dosyasını okuyup tablo varlığına göre çalıştırır."""
        with open(file_path, 'r') as file:
            sql_script = file.read()

        cursor = conn.cursor()
        for statement in sql_script.split(";"):
            if statement.strip():
                # CREATE TABLE ifadesi olup olmadığını kontrol et
                if statement.strip().upper().startswith("CREATE TABLE"):
                    # Tablo adını analiz et
                    table_name = statement.split()[2]  # CREATE TABLE table_name ...
                    table_name = table_name.strip("`")  # Tırnakları kaldır
                    # Tablonun var olup olmadığını kontrol et
                    if table_exists(table_name):
                        print(f"Tablo '{table_name}' zaten mevcut, oluşturulmayacak.")
                        continue
                cursor.execute(statement)
        conn.commit()
        cursor.close()

    # SQL dosyasının göreceli yolunu ayarlama
    sql_file_path = os.path.join(os.path.dirname(__file__), 'database/create_tables.sql')

    try:
        # SQL dosyasını çalıştır
        execute_sql_file(sql_file_path)
        print("Tablolar başarıyla oluşturuldu.")
    except Error as e:
        print(f"Tablo oluşturma hatası: {e}")
    finally:
        if conn.is_connected():
            conn.close()
            print("Bağlantı kapatıldı.")
# Migration dosyalarını da burada çağıracağız zamanı gelince