"""
queries.py
Kumpulan fungsi query database untuk Color Ball Sort Puzzle.
Semua fungsi mengembalikan None / False jika terjadi kegagalan koneksi,
supaya lapisan screens/ bisa menampilkan pesan error dengan aman.
"""

import hashlib
from database.connection import get_connection


# ------------------------------------------------------------
# UTIL
# ------------------------------------------------------------
def hash_password(password: str) -> str:
    """Meng-hash password menggunakan SHA-256."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# ------------------------------------------------------------
# USERS - REGISTER & LOGIN
# ------------------------------------------------------------
def register_user(username: str, password: str):
    """
    Mendaftarkan user baru.
    Return: (True, "pesan sukses") atau (False, "pesan error")
    """
    conn = get_connection()
    if conn is None:
        return False, "Tidak bisa terhubung ke database."

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return False, "Nama pengguna sudah terpakai."

        hashed = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed),
        )
        conn.commit()
        user_id = cursor.lastrowid

        # Buat baris progress awal untuk user ini
        cursor.execute(
            "INSERT INTO progress (user_id, current_level, best_score) "
            "VALUES (%s, 'Easy', 0)",
            (user_id,),
        )
        conn.commit()
        return True, "Registrasi berhasil! Silakan masuk."
    except Exception as e:
        return False, f"Gagal mendaftar: {e}"
    finally:
        cursor.close()
        conn.close()


def login_user(username: str, password: str):
    """
    Memverifikasi login.
    Return: (True, user_dict) jika berhasil, (False, "pesan error") jika gagal.
    """
    conn = get_connection()
    if conn is None:
        return False, "Tidak bisa terhubung ke database."

    try:
        cursor = conn.cursor(dictionary=True)
        hashed = hash_password(password)
        cursor.execute(
            "SELECT id, username, tanggal_daftar FROM users "
            "WHERE username = %s AND password = %s",
            (username, hashed),
        )
        user = cursor.fetchone()
        if user:
            return True, user
        return False, "Nama pengguna atau kata sandi salah."
    except Exception as e:
        return False, f"Gagal login: {e}"
    finally:
        cursor.close()
        conn.close()


# ------------------------------------------------------------
# LEVELS
# ------------------------------------------------------------
def get_all_levels():
    """Mengambil semua data level, urut berdasarkan id_level."""
    conn = get_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM levels ORDER BY id_level ASC")
        return cursor.fetchall()
    except Exception as e:
        print(f"[ERROR] get_all_levels: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def get_level_by_name(nama_level: str):
    conn = get_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM levels WHERE nama_level = %s", (nama_level,))
        return cursor.fetchone()
    except Exception as e:
        print(f"[ERROR] get_level_by_name: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


# ------------------------------------------------------------
# SCORES
# ------------------------------------------------------------
def insert_score(user_id: int, score: int, level_reached: str):
    conn = get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO scores (user_id, score, level_reached) VALUES (%s, %s, %s)",
            (user_id, score, level_reached),
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"[ERROR] insert_score: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def get_top_scores(limit: int = 10):
    """Mengambil top-N skor tertinggi beserta nama pemain untuk leaderboard."""
    conn = get_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT s.score, s.level_reached, s.tanggal_main, u.username
            FROM scores s
            JOIN users u ON s.user_id = u.id
            ORDER BY s.score DESC
            LIMIT %s
            """,
            (limit,),
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"[ERROR] get_top_scores: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def get_user_rank(user_id: int):
    """Menghitung peringkat user berdasarkan skor tertinggi miliknya."""
    conn = get_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT MAX(score) AS best FROM scores WHERE user_id = %s
            """,
            (user_id,),
        )
        row = cursor.fetchone()
        best = row["best"] if row and row["best"] else 0

        cursor.execute(
            """
            SELECT COUNT(*) AS rank_count FROM (
                SELECT user_id, MAX(score) AS max_score
                FROM scores GROUP BY user_id
            ) AS best_scores
            WHERE max_score > %s
            """,
            (best,),
        )
        row2 = cursor.fetchone()
        rank = (row2["rank_count"] if row2 else 0) + 1
        return rank
    except Exception as e:
        print(f"[ERROR] get_user_rank: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_score_history(user_id: int, limit: int = 10):
    conn = get_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT score, level_reached, tanggal_main
            FROM scores
            WHERE user_id = %s
            ORDER BY tanggal_main DESC
            LIMIT %s
            """,
            (user_id, limit),
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"[ERROR] get_score_history: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


# ------------------------------------------------------------
# PROGRESS
# ------------------------------------------------------------
def get_progress(user_id: int):
    conn = get_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM progress WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()
        if row:
            return row

        # Jika belum ada baris progress, buat baru
        cursor.execute(
            "INSERT INTO progress (user_id, current_level, best_score) "
            "VALUES (%s, 'Easy', 0)",
            (user_id,),
        )
        conn.commit()
        cursor.execute("SELECT * FROM progress WHERE user_id = %s", (user_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"[ERROR] get_progress: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def update_progress(user_id: int, current_level: str, best_score: int):
    """
    Menyimpan progress user. `current_level` yang dikirim di sini harus sudah
    berupa hasil keputusan logic/progress_manager.py (level tertinggi yang
    sudah dicapai), supaya tidak salah urutan seperti perbandingan alfabetis
    ('Hard' < 'Medium' secara string, padahal urutannya harus Easy < Medium < Hard).
    """
    conn = get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO progress (user_id, current_level, best_score)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                current_level = VALUES(current_level),
                best_score = GREATEST(VALUES(best_score), best_score)
            """,
            (user_id, current_level, best_score),
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"[ERROR] update_progress: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def get_total_playtime_seconds(user_id: int):
    """Estimasi total waktu bermain (bukan field asli di DB, dihitung dari jumlah sesi)."""
    conn = get_connection()
    if conn is None:
        return 0
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT COUNT(*) AS total_sesi FROM scores WHERE user_id = %s",
            (user_id,),
        )
        row = cursor.fetchone()
        return (row["total_sesi"] if row else 0)
    except Exception as e:
        print(f"[ERROR] get_total_playtime_seconds: {e}")
        return 0
    finally:
        cursor.close()
        conn.close()