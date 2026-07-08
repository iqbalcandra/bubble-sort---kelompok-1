import sys
import os

try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
except ImportError:
    mysql = None
    MySQLError = Exception
    print("[PERINGATAN] Library 'mysql-connector-python' belum terinstall.")
    print("Jalankan: pip install mysql-connector-python")

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",          # sesuaikan dengan password MySQL lokal kamu
    "database": "color_ball_sort",
}

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")
DATA_PATH = os.path.join(os.path.dirname(__file__), "data_contoh.sql")


def _run_sql_file(cursor, path):
    """Menjalankan file .sql statement per statement (dipisah oleh ';')."""
    with open(path, "r", encoding="utf-8") as f:
        sql_content = f.read()

    statements = [s.strip() for s in sql_content.split(";") if s.strip()
                  and not s.strip().startswith("--")]
    for statement in statements:
        try:
            cursor.execute(statement)
        except MySQLError as e:
            # Lewati error "already exists" / duplicate agar idempotent
            if "already exists" not in str(e) and "Duplicate" not in str(e):
                print(f"[SQL WARNING] {e}")


def init_database():
    """Membuat database & tabel jika belum ada, lalu mengisi data awal level."""
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
        )
        cursor = conn.cursor()
        _run_sql_file(cursor, SCHEMA_PATH)
        conn.commit()
        cursor.execute(f"USE {DB_CONFIG['database']}")
        _run_sql_file(cursor, DATA_PATH)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except MySQLError as e:
        print("=" * 60)
        print("[ERROR] Tidak bisa terhubung / inisialisasi database MySQL.")
        print(f"Detail: {e}")
        print("Pastikan MySQL Server aktif dan DB_CONFIG di connection.py benar.")
        print("=" * 60)
        return False
    except Exception as e:
        print(f"[ERROR] Kesalahan tak terduga saat init database: {e}")
        return False


def get_connection():
    """Mengembalikan objek koneksi MySQL aktif ke database color_ball_sort."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except MySQLError as e:
        print(f"[ERROR] Gagal konek ke database: {e}")
        return None
