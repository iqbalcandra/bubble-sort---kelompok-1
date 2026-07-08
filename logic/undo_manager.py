"""
logic/undo_manager.py
Mengelola fitur Undo (membatalkan satu langkah terakhir).

Sesuai laporan BAB 5.4:
- Pemain hanya bisa membatalkan SATU langkah terakhir.
- Fitur ini tidak mempengaruhi timer maupun skor dasar.

API dipakai di screens/game_screen.py:
    undo_manager.save_state(self.tubes)   -> simpan kondisi papan sebelum bergerak
    undo_manager.undo()                   -> kembalikan kondisi papan sebelumnya
    undo_manager.clear()                  -> kosongkan riwayat (dipanggil saat reset_level)
"""

import copy


class UndoManager:
    def __init__(self, batas_riwayat: int = 1):
        """
        :param batas_riwayat: jumlah maksimal langkah yang bisa di-undo.
                               Default 1, sesuai laporan (hanya 1 langkah terakhir).
        """
        self.batas_riwayat = batas_riwayat
        self._riwayat = []  # stack kondisi papan sebelum tiap langkah

    def save_state(self, tubes: list) -> None:
        """
        Menyimpan kondisi papan (tubes) SEBELUM sebuah langkah dilakukan.
        Dipanggil oleh game_screen.py tepat sebelum move_ball() mengubah papan.

        :param tubes: representasi papan saat ini (list of list, tiap tabung
                      berisi list warna dari bawah ke atas)
        """
        # Simpan salinan independen (deep copy) supaya tidak ikut berubah
        # saat tubes asli dimodifikasi setelah ini.
        self._riwayat.append(copy.deepcopy(tubes))

        # Batasi jumlah riwayat sesuai batas_riwayat, buang yang paling lama
        if len(self._riwayat) > self.batas_riwayat:
            self._riwayat.pop(0)

    def bisa_undo(self) -> bool:
        """Mengecek apakah ada langkah yang bisa dibatalkan."""
        return len(self._riwayat) > 0

    def undo(self):
        """
        Mengembalikan kondisi papan (tubes) ke sebelum langkah terakhir.
        Tidak mempengaruhi timer maupun skor dasar level.

        :return: kondisi tubes sebelumnya, atau None jika tidak ada riwayat
        """
        if not self.bisa_undo():
            return None

        return self._riwayat.pop()

    def clear(self) -> None:
        """
        Mengosongkan seluruh riwayat undo.
        Dipanggil saat level baru dimulai atau saat 'Ulangi Level' ditekan
        (reset_level di game_screen.py).
        """
        self._riwayat = []
