"""
logic/progress_manager.py
Mengelola progres permainan pemain: level tertinggi yang sudah dicapai
dan skor terbaik, disimpan ke tabel `progress` lewat database/queries.py.

API dipakai di screens/game_screen.py:
    progress_manager.update_progress(user_id=..., next_level=..., score=...)

PENTING: current_level TIDAK langsung ditimpa mentah-mentah. Level hanya
maju (tidak pernah mundur) walau pemain main ulang level yang lebih rendah
setelah pernah mencapai level lebih tinggi. Perbandingan urutan level
memakai id_level dari tabel `levels` (Mudah=1, Sedang=2, Sulit=3), BUKAN
perbandingan alfabetis string (yang akan salah, karena 'Sulit' < 'Sedang'
secara alfabet padahal urutannya harus lebih tinggi).
"""

from database import queries


class ProgressManager:
    def __init__(self):
        pass

    def update_progress(self, user_id: int, next_level: str, score: int) -> bool:
        """
        Memperbarui progres pemain setelah menyelesaikan sebuah level.

        :param user_id: id pemain yang sedang login
        :param next_level: nama level "tujuan" hasil dari level_manager.next_level()
                            (bisa sama dengan level saat ini jika sudah di level terakhir)
        :param score: skor yang baru saja didapat pemain
        :return: True jika berhasil disimpan, False jika gagal
        """
        progress_sekarang = queries.get_progress(user_id)

        if progress_sekarang is None:
            level_final = next_level
            best_score_final = score
        else:
            level_final = self._pilih_level_tertinggi(
                progress_sekarang.get("current_level"), next_level
            )
            best_score_final = max(progress_sekarang.get("best_score", 0), score)

        return queries.update_progress(
            user_id=user_id,
            current_level=level_final,
            best_score=best_score_final,
        )

    def _pilih_level_tertinggi(self, level_a: str, level_b: str) -> str:
        """
        Membandingkan dua nama level berdasarkan id_level di tabel `levels`,
        mengembalikan nama level yang urutannya lebih tinggi/lanjut.
        """
        info_a = queries.get_level_by_name(level_a) if level_a else None
        info_b = queries.get_level_by_name(level_b) if level_b else None

        id_a = info_a["id_level"] if info_a else 0
        id_b = info_b["id_level"] if info_b else 0

        if id_b >= id_a:
            return level_b
        return level_a

    def get_progress_pemain(self, user_id: int):
        """
        Mengambil progres pemain saat ini (current_level & best_score).
        Berguna untuk screens/level_screen.py (cek lock/unlock) dan
        screens/menu_screen.py / progress screen (tampilkan ringkasan progres).
        """
        return queries.get_progress(user_id)