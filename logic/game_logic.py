"""
logic/game_logic.py
Logika inti permainan Color Ball Sort Puzzle — murni logic, TIDAK ada
kode Tkinter/GUI di file ini. Dipanggil oleh screens/game_screen.py.

Representasi papan (tubes):
    tubes = list of list
    Setiap tabung berisi list warna (str hex, mis. "#FF5252"), disusun
    dari bawah ke atas. Contoh:
        tubes[0] = ["#FF5252", "#4CAF50", "#FF5252"]

API dipakai di screens/game_screen.py:
    game_logic = GameLogic()
    game_logic.generate_tubes(jumlah_warna, jumlah_tabung)
    game_logic.move_ball(tubes, sumber, tujuan)   -> bool, tubes diubah in-place
    game_logic.check_win(tubes)                   -> bool
"""

import random

DAFTAR_WARNA = [
    "#FF5252",  # Merah
    "#2196F3",  # Biru
    "#FFC107",  # Kuning
]

KAPASITAS_TABUNG = 4


class GameLogic:
    def __init__(self, kapasitas_tabung: int = KAPASITAS_TABUNG):
        self.kapasitas_tabung = kapasitas_tabung

    def generate_tubes(self, jumlah_warna: int, jumlah_tabung: int) -> list:
        """
        Membuat susunan awal papan (tubes) permainan secara acak.
        """

        # Validasi jumlah warna
        if jumlah_warna > len(DAFTAR_WARNA):
            raise ValueError(
                f"Jumlah warna ({jumlah_warna}) melebihi aset yang tersedia ({len(DAFTAR_WARNA)})."
            )

        warna = DAFTAR_WARNA[:jumlah_warna]

        semua_bola = []
        for warna_bola in warna:
            for _ in range(self.kapasitas_tabung):
                semua_bola.append(warna_bola)

        random.shuffle(semua_bola)

        tubes = []
        for i in range(jumlah_warna):
            tubes.append(
                semua_bola[i * self.kapasitas_tabung:(i + 1) * self.kapasitas_tabung]
            )

        jumlah_kosong = jumlah_tabung - jumlah_warna
        for _ in range(jumlah_kosong):
            tubes.append([])

        return tubes

    def validasi_pindah(self, tubes: list, sumber: int, tujuan: int) -> bool:

        if sumber == tujuan:
            return False

        asal = tubes[sumber]
        target = tubes[tujuan]

        if len(asal) == 0:
            return False

        if len(target) >= self.kapasitas_tabung:
            return False

        return True

    def move_ball(self, tubes: list, sumber: int, tujuan: int) -> bool:
        """
        Mengeksekusi perpindahan satu bola dari tabung sumber ke tujuan.
        `tubes` diubah langsung (in-place). Method ini sudah termasuk
        validasi di dalamnya, jadi cukup dipanggil langsung dari game_screen.py
        seperti: berhasil = self.game_logic.move_ball(self.tubes, sumber, tujuan)

        :return: True jika langkah valid & berhasil dieksekusi, False jika tidak
        """
        if not self.validasi_pindah(tubes, sumber, tujuan):
            return False

        bola = tubes[sumber].pop()
        tubes[tujuan].append(bola)
        return True

    def check_win(self, tubes: list) -> bool:
        """
        Level dinyatakan selesai jika setiap tabung yang tidak kosong
        hanya berisi 1 warna dan penuh (kapasitas_tabung).
        """
        for tube in tubes:
            if len(tube) == 0:
                continue
            if len(set(tube)) != 1:
                return False
            if len(tube) != self.kapasitas_tabung:
                return False
        return True
