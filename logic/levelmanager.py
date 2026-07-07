"""
logic/level_manager.py
Mengelola konfigurasi level & mapping nama level.

Catatan penting:
- Di DATABASE, nama_level disimpan dalam Bahasa Inggris: 'Easy', 'Medium', 'Hard'
  (mengikuti laporan & data_contoh.sql).
- Di DESAIN UI, label level ditampilkan dalam Bahasa Indonesia:
  'Mudah', 'Sedang', 'Sulit' (dipakai di screens/game_screen.py & level_screen.py).

Modul ini menjembatani dua penamaan tersebut, supaya database tetap konsisten
dengan laporan, sementara tampilan tetap sesuai desain UI/UX.
"""

from database.queries import get_all_levels, get_level_by_name

LEVELS = [
    {"urutan": 1, "nama_db": "Easy",   "nama_tampil": "Mudah"},
    {"urutan": 2, "nama_db": "Medium", "nama_tampil": "Sedang"},
    {"urutan": 3, "nama_db": "Hard",   "nama_tampil": "Sulit"},
]

TAMPIL_KE_DB = {lvl["nama_tampil"]: lvl["nama_db"] for lvl in LEVELS}
DB_KE_TAMPIL = {lvl["nama_db"]: lvl["nama_tampil"] for lvl in LEVELS}
URUTAN_DB = {lvl["nama_db"]: lvl["urutan"] for lvl in LEVELS}


def get_nama_tampil(nama_level: str) -> str:
    """Mengubah nama level DB ('Easy') menjadi nama tampilan ('Mudah')."""
    return DB_KE_TAMPIL.get(nama_level, nama_level)


def get_nama_db(nama_level: str) -> str:
    """Mengubah nama level tampilan ('Mudah') menjadi nama DB ('Easy')."""
    return TAMPIL_KE_DB.get(nama_level, nama_level)


def level_lebih_tinggi(level_a_db: str, level_b_db: str) -> str:
    """Mengembalikan nama_db level yang urutannya lebih tinggi di antara dua level."""
    urutan_a = URUTAN_DB.get(level_a_db, 0)
    urutan_b = URUTAN_DB.get(level_b_db, 0)
    return level_a_db if urutan_a >= urutan_b else level_b_db


def next_level_db(nama_db: str):
    """Mengembalikan nama_db level berikutnya, atau None jika sudah level terakhir."""
    urutan_sekarang = URUTAN_DB.get(nama_db, 0)
    for lvl in LEVELS:
        if lvl["urutan"] == urutan_sekarang + 1:
            return lvl["nama_db"]
    return None


def level_terkunci(nama_db: str, current_level_db: str) -> bool:
    """
    True jika level `nama_db` masih terkunci untuk pemain, berdasarkan
    `current_level_db` (level tertinggi yang pernah dicapai pemain).
    Level pertama (Easy) selalu terbuka.
    """
    return URUTAN_DB.get(nama_db, 0) > URUTAN_DB.get(current_level_db, 1)


def build_level_data(level_row: dict) -> dict:
    """
    Mengubah satu baris tabel `levels` dari database menjadi dict siap pakai
    untuk GameScreen, dengan nama_level dalam Bahasa Indonesia supaya cocok
    dengan badge warna & label di desain UI.
    """
    return {
        "id_level": level_row["id_level"],
        "nama_level": get_nama_tampil(level_row["nama_level"]),
        "nama_level_db": level_row["nama_level"],
        "jumlah_warna": level_row["jumlah_warna"],
        "jumlah_tabung": level_row["jumlah_tabung"],
        "timer": level_row["timer"],
        "skor_dasar": level_row["skor_dasar"],
    }


def get_semua_level_data():
    """Mengambil semua level dari database, sudah dalam format siap pakai UI."""
    rows = get_all_levels()
    return [build_level_data(row) for row in rows]


def get_level_data_by_nama_tampil(nama_tampil: str):
    """Mengambil satu level (format siap pakai UI) berdasarkan nama tampilan Indonesia."""
    nama_db = get_nama_db(nama_tampil)
    row = get_level_by_name(nama_db)
    if row is None:
        return None
    return build_level_data(row)
