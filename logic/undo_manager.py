"""
logic/undo_manager.py

Mengatur fitur Undo pada game Color Ball Sort Puzzle.

Tugas:
- Menyimpan kondisi board sebelum langkah dilakukan
- Mengembalikan board ke kondisi sebelumnya
- Menghapus riwayat saat reset level

Tidak menggunakan Tkinter.
"""

import copy


class UndoManager:

    def __init__(self, maksimal_undo=50):

        # penyimpanan history board
        self.history = []

        # batas penyimpanan undo
        self.maksimal_undo = maksimal_undo


    # ==========================================
    # SIMPAN STATE SEBELUM PINDAH
    # ==========================================

    def save_state(self, tubes):

        """
        Menyimpan kondisi tubes sebelum perpindahan.

        Menggunakan deepcopy agar data lama tidak
        ikut berubah ketika bola dipindahkan.
        """

        state = copy.deepcopy(tubes)

        self.history.append(state)


        # batasi jumlah undo
        if len(self.history) > self.maksimal_undo:

            self.history.pop(0)



    # ==========================================
    # KEMBALI KE STATE SEBELUMNYA
    # ==========================================

    def undo(self):

        """
        Mengambil board terakhir yang tersimpan.

        Return:
        - list tubes jika tersedia
        - None jika tidak ada history
        """

        if len(self.history) == 0:

            return None


        return self.history.pop()



    # ==========================================
    # HAPUS HISTORY
    # ==========================================

    def clear(self):

        """
        Menghapus semua riwayat undo.
        Dipanggil ketika:
        - reset level
        - mulai level baru
        """

        self.history.clear()



    # ==========================================
    # CEK JUMLAH UNDO
    # ==========================================

    def can_undo(self):

        """
        Mengecek apakah masih bisa undo.
        """

        return len(self.history) > 0



    def jumlah_undo(self):

        """
        Mengembalikan jumlah history tersedia.
        """

        return len(self.history)
