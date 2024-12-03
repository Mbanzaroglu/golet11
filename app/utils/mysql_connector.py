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
        password="",
        database="bp_database",
        ssl_disabled=True  # SSL'i devre dışı bırak
    )

    def table_exists(table_name):
        # Tablo varlığını kontrol et
        cursor = conn.cursor()
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def execute_sql_file(file_path):
        # SQL dosyasını çalıştır
        with open(file_path, 'r') as file:
            sql_script = file.read()

        cursor = conn.cursor()
        for statement in sql_script.split(";"):
            if statement.strip():
                # CREATE TABLE için kontrol
                if statement.strip().upper().startswith("CREATE TABLE"):
                    table_name = statement.split()[2].strip("`")  # Tablo adını al
                    if table_exists(table_name):
                        print(f"Tablo '{table_name}' zaten mevcut, oluşturulmayacak.")
                        continue
                cursor.execute(statement)
        conn.commit()
        cursor.close()

    # Migration tablosunun varlığını kontrol et ve yoksa oluştur
    if not table_exists('migrations'):
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE migrations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            migration_name VARCHAR(255) NOT NULL UNIQUE
        )
        """)
        conn.commit()
        cursor.close()
        print("Migration tablosu başarıyla oluşturuldu.")
    else:
        print("Migration tablosu zaten mevcut, oluşturulmayacak.")

    # Tabloları oluşturmak için SQL dosyasını çalıştır
    sql_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database/create_tables.sql')
    try:
        execute_sql_file(sql_file_path)
        print("Tablolar başarıyla oluşturuldu.")
    except Error as e:
        print(f"Tablo oluşturma hatası: {e}")

    # Migration işlemlerini başlat
    migrations(conn)

def migrations(conn):
    """
    Migration dosyalarını kontrol edip çalıştırır.
    Daha önce çalıştırılmış olanları atlar.
    """
    migrations_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database/migrations')

    # Migration tablosunun varlığını kontrol et ve yoksa oluştur
    def ensure_migrations_table_exists():
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS migrations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            migration_name VARCHAR(255) NOT NULL UNIQUE)
        """)
        conn.commit()
        cursor.close()

    # Daha önce çalıştırılmış migrationları getir
    def get_executed_migrations():
        cursor = conn.cursor()
        cursor.execute("SELECT migration_name FROM migrations")
        result = {row[0] for row in cursor.fetchall()}
        cursor.close()
        return result

    # Migration dosyasını çalıştır ve kaydet
    def execute_and_record_migration(file_path, file_name):
        if not os.path.exists(file_path):
            print(f"Migration dosyası bulunamadı: {file_path}")
            return

        with open(file_path, 'r') as file:
            sql_script = file.read()

        cursor = conn.cursor()
        try:
            for statement in sql_script.split(";"):
                if statement.strip():
                    cursor.execute(statement)
            conn.commit()

            # Migration'ı kaydet
            cursor.execute("INSERT INTO migrations (migration_name) VALUES (%s)", (file_name,))
            conn.commit()
            print(f"Migration '{file_name}' başarıyla çalıştırıldı.")
        except Error as e:
            conn.rollback()
            print(f"Migration '{file_name}' çalıştırılırken hata oluştu: {e}")
            print(f"Hata detayları: Dosya: {file_path}")
        finally:
            cursor.close()

    # İşlemleri gerçekleştir
    ensure_migrations_table_exists()

    if not os.path.exists(migrations_dir) or not os.listdir(migrations_dir):
        print("Migration klasörü bulunamadı veya boş.")
        return

    executed_migrations = get_executed_migrations()

    for filename in sorted(os.listdir(migrations_dir)):
        if filename.endswith(".sql") and filename not in executed_migrations:
            file_path = os.path.join(migrations_dir, filename)
            execute_and_record_migration(file_path, filename)