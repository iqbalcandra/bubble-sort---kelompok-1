"""
queries.py
Kumpulan fungsi query database untuk Color Ball Sort Puzzle.
Semua fungsi mengembalikan None / False jika terjadi kegagalan koneksi,
supaya lapisan screens/ bisa menampilkan pesan error dengan aman.
"""

import hashlib
from database.connection import get_connection

# Nama level default HARUS sama persis dengan data di tabel `levels`
# (lihat data_contoh.sql: 'Mudah', 'Sedang', 'Sulit')
LEVEL_AWAL_DEFAULT = "Mudah"


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
        # PENTING: pakai LEVEL_AWAL_DEFAULT ('Mudah'), harus cocok dengan tabel levels
        cursor.execute(
            "INSERT INTO progress (user_id, current_level, best_score) "
            "VALUES (%s, %s, 0)",
            (user_id, LEVEL_AWAL_DEFAULT),
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
    """
    Menyimpan skor ke tabel scores.
    Kolom waktu (waktu_bermain) otomatis terisi CURRENT_TIMESTAMP oleh MySQL,
    tidak perlu dikirim manual dari Python.
    """
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


# Alias: logic/score_manager.py memanggil queries.simpan_skor(user_id=..., score=..., level_reached=...)
# Disediakan supaya score_manager.py tidak perlu diubah.
def simpan_skor(user_id: int, score: int, level_reached: str) -> bool:
    return insert_score(user_id, score, level_reached)


def get_top_scores(limit: int = 5):
    """Mengambil top-N skor tertinggi beserta nama pemain untuk leaderboard (default Top 5)."""
    conn = get_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT s.score, s.level_reached, s.waktu_bermain, u.username
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
            "SELECT MAX(score) AS best FROM scores WHERE user_id = %s",
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
            SELECT score, level_reached, waktu_bermain
            FROM scores
            WHERE user_id = %s
            ORDER BY waktu_bermain DESC
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

        # Jika belum ada baris progress, buat baru dengan level awal default
        cursor.execute(
            "INSERT INTO progress (user_id, current_level, best_score) "
            "VALUES (%s, %s, 0)",
            (user_id, LEVEL_AWAL_DEFAULT),
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
    sudah dicapai), supaya tidak salah urutan seperti perbandingan alfabetis.

    Catatan: memakai alias row "AS baru" (bukan VALUES()) karena fungsi
    VALUES() di ON DUPLICATE KEY UPDATE sudah deprecated sejak MySQL 8.0.20.
    """
    conn = get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO progress (user_id, current_level, best_score)
            VALUES (%s, %s, %s) AS baru
            ON DUPLICATE KEY UPDATE
                current_level = baru.current_level,
                best_score = GREATEST(baru.best_score, progress.best_score)
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
    """
    Estimasi jumlah sesi bermain (BUKAN durasi asli dalam detik, karena
    tabel scores tidak menyimpan durasi per sesi, hanya waktu selesai).
    Nama fungsi dipertahankan agar tidak mengubah pemanggil lain, tapi
    nilainya adalah jumlah sesi, bukan detik.
    """
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


# ------------------------------------------------------------
# Alias tambahan (kompatibilitas dengan penamaan sebelumnya)
# ------------------------------------------------------------
daftar_user = register_user
ambil_semua_level = get_all_levels
ambil_level_by_nama = get_level_by_name
ambil_leaderboard = get_top_scores
ambil_progress = get_progress
