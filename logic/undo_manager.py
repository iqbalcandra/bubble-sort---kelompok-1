"""
undo_manager.py
Mengelola fitur Undo (membatalkan satu langkah terakhir).

Sesuai laporan BAB 5.4:
- Pemain hanya bisa membatalkan SATU langkah terakhir.
- Fitur ini tidak mempengaruhi timer maupun skor dasar.
"""

import copy


class UndoManager:
    def __init__(self, batas_riwayat: int = 1):
        """
        :param batas_riwayat: jumlah maksimal langkah yang disimpan untuk di-undo.
                               Default 1, sesuai laporan (hanya bisa undo 1 langkah).
        """
        self.batas_riwayat = batas_riwayat
        self._riwayat_papan = []  # stack kondisi papan sebelum tiap langkah

    def simpan_state(self, kondisi_papan: list) -> None:
        """
        Menyimpan kondisi papan (tabung & bola) SEBELUM sebuah langkah dilakukan.
        Dipanggil oleh game_logic.py setiap kali pemain berhasil memindahkan bola.

        :param kondisi_papan: representasi papan saat ini, mis. list of list
                               (tiap tabung berisi list warna bola dari bawah ke atas)
        """
        # Simpan salinan independen (deep copy) agar tidak ikut berubah
        # saat papan asli dimodifikasi setelah ini.
        self._riwayat_papan.append(copy.deepcopy(kondisi_papan))

        # Batasi riwayat sesuai batas_riwayat, buang yang paling lama jika kelebihan
        if len(self._riwayat_papan) > self.batas_riwayat:
            self._riwayat_papan.pop(0)

    def bisa_undo(self) -> bool:
        """Mengecek apakah ada langkah yang bisa dibatalkan."""
        return len(self._riwayat_papan) > 0

    def undo(self):
        """
        Mengembalikan kondisi papan ke sebelum langkah terakhir dilakukan.
        Tidak mengubah timer maupun skor dasar level.

        :return: kondisi_papan sebelumnya, atau None jika tidak ada riwayat
        """
        if not self.bisa_undo():
            return None

        return self._riwayat_papan.pop()

    def reset(self) -> None:
        """
        Mengosongkan seluruh riwayat undo.
        Dipanggil saat level baru dimulai atau saat 'Ulangi Level' ditekan.
        """
        self._riwayat_papan = []
