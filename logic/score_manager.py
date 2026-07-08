"""
logic/score_manager.py
Mengelola perhitungan skor level & penyimpanan skor ke database.

Rumus (sesuai laporan BAB IV):
    Total Skor = Skor Dasar + (Sisa Waktu x 10)

API disesuaikan dengan pemanggilan di screens/game_screen.py:
    score_manager.set_level(level_data)
    score_manager.hitung_skor(sisa_waktu)   -> mengembalikan int total_score
    score_manager.simpan_skor(user_id, level_reached)
"""

from database import queries


class ScoreManager:
    def __init__(self):
        self.level_data = None
        self.skor_dasar = 0

        # Rincian & hasil skor dari perhitungan TERAKHIR (dipakai saat simpan
        # ke database, dan bisa dipakai result_screen.py untuk breakdown skor)
        self.skor_terakhir = 0
        self.bonus_waktu_terakhir = 0

    def set_level(self, level_data: dict) -> None:
        """
        Menyimpan konfigurasi level yang sedang dimainkan.
        Dipanggil di start_level() sebelum level dimulai.

        :param level_data: dict berisi minimal {"skor_dasar": int, ...}
        """
        self.level_data = level_data
        self.skor_dasar = level_data.get("skor_dasar", 0)

    def hitung_skor(self, sisa_waktu: int) -> int:
        """
        Menghitung total skor berdasarkan sisa waktu saat level selesai.
        Dipanggil dari win_game() di game_screen.py.

        :param sisa_waktu: sisa waktu dalam detik saat pemain menang
        :return: total skor (int)
        """
        if sisa_waktu < 0:
            sisa_waktu = 0

        bonus_waktu = sisa_waktu * 10
        total_skor = self.skor_dasar + bonus_waktu

        # simpan untuk dipakai saat simpan_skor() / breakdown UI
        self.bonus_waktu_terakhir = bonus_waktu
        self.skor_terakhir = total_skor

        return total_skor

    def simpan_skor(self, user_id: int, level_reached: str) -> bool:
        """
        Menyimpan skor hasil hitung_skor() terakhir ke tabel `scores`.
        Hanya dipanggil saat level SELESAI (menang) — tidak dipanggil saat
        Game Over atau reset level, sesuai laporan.

        :param user_id: id pemain yang sedang login
        :param level_reached: nama level yang berhasil diselesaikan (mis. "Mudah")
        :return: True jika berhasil disimpan, False jika gagal
        """
        return queries.simpan_skor(
            user_id=user_id,
            score=self.skor_terakhir,
            level_reached=level_reached,
        )

    def get_rincian_skor(self) -> dict:
        """
        Mengembalikan rincian skor perhitungan terakhir, berguna untuk
        ditampilkan di Victory Screen (Skor Dasar, Bonus Waktu, Total Skor).
        """
        return {
            "skor_dasar": self.skor_dasar,
            "bonus_waktu": self.bonus_waktu_terakhir,
            "total_skor": self.skor_terakhir,
        }

    def get_skor_terakhir(self) -> int:
        """Mengembalikan total skor hasil perhitungan terakhir."""
        return self.skor_terakhir
