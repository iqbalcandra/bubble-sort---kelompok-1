"""
score_manager.py
Mengelola perhitungan skor, akumulasi skor sesi, dan penyimpanan skor ke database.

Rumus (sesuai laporan BAB IV):
    Total Skor = Skor Dasar + (Sisa Waktu x 10)
"""

from database import queries


class ScoreManager:
    def __init__(self):
        # Skor total yang terakumulasi selama satu sesi bermain (bisa lebih dari 1 level)
        self.total_skor_sesi = 0
        # Riwayat rincian skor tiap level yang sudah diselesaikan pada sesi ini
        self.riwayat_skor = []

    def hitung_skor_level(self, skor_dasar: int, sisa_waktu: int) -> dict:
        """
        Menghitung skor untuk satu level yang berhasil diselesaikan.

        :param skor_dasar: skor dasar level (dari tabel levels, kolom skor_dasar)
        :param sisa_waktu: sisa waktu dalam detik saat level selesai
        :return: dict berisi rincian skor (skor_dasar, bonus_waktu, total_skor)
        """
        if sisa_waktu < 0:
            sisa_waktu = 0

        bonus_waktu = sisa_waktu * 10
        total_skor = skor_dasar + bonus_waktu

        rincian = {
            "skor_dasar": skor_dasar,
            "bonus_waktu": bonus_waktu,
            "total_skor": total_skor,
        }
        return rincian

    def tambah_skor(self, rincian_skor: dict) -> None:
        """
        Menambahkan hasil skor satu level ke akumulasi skor sesi.
        Dipanggil setelah hitung_skor_level() saat pemain menang (Victory Screen).
        """
        self.total_skor_sesi += rincian_skor["total_skor"]
        self.riwayat_skor.append(rincian_skor)

    def reset_sesi(self) -> None:
        """Reset akumulasi skor, dipanggil saat pemain memulai sesi permainan baru."""
        self.total_skor_sesi = 0
        self.riwayat_skor = []

    def simpan_skor_ke_database(self, user_id: int, level_reached: str) -> None:
        """
        Menyimpan skor ke tabel `scores` di database.
        Hanya dipanggil saat level SELESAI (menang). Skor tidak disimpan saat
        pemain gagal (Game Over) atau melakukan reset level, sesuai laporan.

        :param user_id: id pemain yang sedang login
        :param level_reached: nama level yang berhasil diselesaikan (mis. "Mudah")
        """
        skor_terakhir = self.riwayat_skor[-1]["total_skor"] if self.riwayat_skor else 0
        queries.simpan_skor(
            user_id=user_id,
            score=skor_terakhir,
            level_reached=level_reached,
        )

    def get_total_skor_sesi(self) -> int:
        """Mengembalikan total skor yang sudah terkumpul pada sesi bermain saat ini."""
        return self.total_skor_sesi
