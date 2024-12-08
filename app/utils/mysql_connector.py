import mysql.connector
from mysql.connector import Error
import os

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="",
            database="bp_database",
            ssl_disabled=True  # SSL'i devre dışı bırak
        )
        return conn
    except Error as e:
        print(f"Veritabanı bağlantı hatası: {e}")
        return None

def table_exists(conn, table_name):
    """Tablonun var olup olmadığını kontrol eder."""
    cursor = conn.cursor()
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    result = cursor.fetchone()
    cursor.close()
    return result is not None

def ensure_migrations_table_exists(conn):
    """Migrations tablosunun varlığını kontrol eder ve yoksa oluşturur."""
    if not table_exists(conn, 'migrations'):
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE migrations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            migration_name VARCHAR(255) NOT NULL UNIQUE
        )
        """)
        conn.commit()
        cursor.close()
        print("Migrations tablosu başarıyla oluşturuldu.")

def execute_sql_file(conn, file_path):
    """Belirtilen SQL dosyasını çalıştırır."""
    if not os.path.exists(file_path):
        print(f"SQL dosyası bulunamadı: {file_path}")
        return

    with open(file_path, 'r') as file:
        sql_script = file.read()

    cursor = conn.cursor()
    try:
        for statement in sql_script.split(";"):
            if statement.strip():
                # CREATE TABLE için kontrol
                if statement.strip().upper().startswith("CREATE TABLE"):
                    table_name = statement.split()[2].strip("`")
                    if table_exists(conn, table_name):
                        continue
                cursor.execute(statement)
        conn.commit()
        # print(f"SQL dosyası başarıyla çalıştırıldı: {file_path}")
    except Error as e:
        conn.rollback()
        print(f"SQL dosyası çalıştırılırken hata oluştu '{file_path}': {e}")
    finally:
        cursor.close()

def get_executed_migrations(conn):
    """Daha önce çalıştırılmış migrationları getirir."""
    cursor = conn.cursor()
    cursor.execute("SELECT migration_name FROM migrations")
    result = {row[0] for row in cursor.fetchall()}
    cursor.close()
    return result

def execute_and_record_migration(conn, file_path, file_name):
    """Migration dosyasını çalıştırır ve kaydeder."""
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
    finally:
        cursor.close()

def migrations(conn):
    """
    Migration dosyalarını kontrol edip çalıştırır.
    Daha önce çalıştırılmış olanları atlar.
    """
    migrations_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'migrations')

    if not os.path.exists(migrations_dir) or not os.listdir(migrations_dir):
        print("Migration klasörü bulunamadı veya boş.")
        return

    executed_migrations = get_executed_migrations(conn)

    for filename in sorted(os.listdir(migrations_dir)):
        if filename.endswith(".sql") and filename not in executed_migrations:
            file_path = os.path.join(migrations_dir, filename)
            execute_and_record_migration(conn, file_path, filename)

def initialize_database():
    """Veritabanını initialize eder ve migrations işlemlerini gerçekleştirir."""
    conn = connect_db()
    if conn is None:
        print("Veritabanına bağlanılamadı.")
        return

    try:
        # Migrations tablosunun varlığını kontrol et ve yoksa oluştur
        ensure_migrations_table_exists(conn)

        # Tabloları oluşturmak için SQL dosyasını çalıştır
        sql_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'create_tables.sql')
        execute_sql_file(conn, sql_file_path)

        # Migration işlemlerini başlat
        migrations(conn)
    finally:
        # Bağlantıyı kapat
        conn.close()
        print("Veritabanı bağlantısı initialize işleminden sonra kapatıldı.")
