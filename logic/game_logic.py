

import random

DAFTAR_WARNA = [
    "#FF5252",  # Merah
    "#2196F3",  # Biru
    "#FFC107",  # Kuning
]  # hanya 3 warna, sesuai jumlah aset gambar bola yang tersedia

KAPASITAS_TABUNG = 4  # maksimal 4 bola per tabung


class GameLogic:
    def __init__(self, kapasitas_tabung: int = KAPASITAS_TABUNG):
        self.kapasitas_tabung = kapasitas_tabung  # simpan kapasitas untuk dipakai di semua method

    def generate_tubes(self, jumlah_warna: int, jumlah_tabung: int) -> list:
        """
        Membuat susunan awal papan (tubes) permainan secara acak.
        """

        # Validasi jumlah warna
        if jumlah_warna > len(DAFTAR_WARNA):  # cegah minta warna melebihi yang tersedia
            raise ValueError(
                f"Jumlah warna ({jumlah_warna}) melebihi aset yang tersedia ({len(DAFTAR_WARNA)})."
            )

        warna = DAFTAR_WARNA[:jumlah_warna]  # ambil sejumlah warna sesuai kebutuhan level

        semua_bola = []
        for warna_bola in warna:  # untuk tiap warna...
            for _ in range(self.kapasitas_tabung):  # buat sebanyak kapasitas_tabung bola
                semua_bola.append(warna_bola)

        random.shuffle(semua_bola)  # acak urutan supaya papan tidak monoton

        tubes = []
        for i in range(jumlah_warna):
            tubes.append(
                semua_bola[i * self.kapasitas_tabung:(i + 1) * self.kapasitas_tabung]
            )  # potong list bola jadi irisan, tiap irisan jadi isi 1 tabung

        jumlah_kosong = jumlah_tabung - jumlah_warna  # sisa tabung yang belum terisi
        for _ in range(jumlah_kosong):
            tubes.append([])  # jadikan tabung kosong sebagai ruang kerja

        return tubes

    def validasi_pindah(self, tubes: list, sumber: int, tujuan: int) -> bool:

        if sumber == tujuan:  # tidak masuk akal pindah ke tabung sendiri
            return False

        asal = tubes[sumber]
        target = tubes[tujuan]

        if len(asal) == 0:  # tidak bisa ambil bola dari tabung kosong
            return False

        if len(target) >= self.kapasitas_tabung:  # tidak bisa isi tabung yang sudah penuh
            return False

        return True  # lolos semua cek, langkah valid (warna tidak dicek di sini)

    def move_ball(self, tubes: list, sumber: int, tujuan: int) -> bool:
        """
        Mengeksekusi perpindahan satu bola dari tabung sumber ke tujuan.
        `tubes` diubah langsung (in-place). Method ini sudah termasuk
        validasi di dalamnya, jadi cukup dipanggil langsung dari game_screen.py
        seperti: berhasil = self.game_logic.move_ball(self.tubes, sumber, tujuan)

        :return: True jika langkah valid & berhasil dieksekusi, False jika tidak
        """
        if not self.validasi_pindah(tubes, sumber, tujuan):  # batalkan kalau tidak valid
            return False

        bola = tubes[sumber].pop()      # ambil bola paling atas dari tabung sumber
        tubes[tujuan].append(bola)      # taruh di paling atas tabung tujuan
        return True

    def check_win(self, tubes: list) -> bool:
        """
        Level dinyatakan selesai jika setiap tabung yang tidak kosong
        hanya berisi 1 warna dan penuh (kapasitas_tabung).
        """
        for tube in tubes:
            if len(tube) == 0:  # tabung kosong boleh, lanjut cek yang lain
                continue
            if len(set(tube)) != 1:  # ada lebih dari 1 warna -> belum rapi
                return False
            if len(tube) != self.kapasitas_tabung:  # belum penuh -> belum selesai
                return False
        return True  # semua tabung rapi & penuh -> menang