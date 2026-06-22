import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager

DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "",
    "database": "color_ball_sort",
}

def get_connection():
    """Buka koneksi ke database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("Koneksi database berhasil")
            return conn
    except Error as e:
        print(f"Gagal koneksi: {e}")
        return None

def close_connection(conn):
    """Tutup koneksi database."""
    if conn and conn.is_connected():
        conn.close()

@contextmanager
def db_connection():
    """Context manager – auto commit, rollback, dan close."""
    conn = None
    try:
        conn = get_connection()
        yield conn
        conn.commit()
    except Error as e:
        if conn:
            conn.rollback()
        print(f"Transaksi gagal: {e}")
        raise
    finally:
        close_connection(conn)

def test_connection():
    """Cek koneksi saat startup."""
    conn = get_connection()
    if conn:
        close_connection(conn)
        return True
    return False

if __name__ == "__main__":
    test_connection()