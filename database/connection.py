import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="color_ball_sort"
        )

        if conn.is_connected():
            print("Koneksi database berhasil")
            return conn

    except Error as e:
        print(f"Gagal koneksi ke database: {e}")
        return None