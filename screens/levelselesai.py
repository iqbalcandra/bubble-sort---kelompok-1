"""
screens/levelselesai.py

Halaman "Level Selesai" — muncul setelah pemain menang di sebuah level.
Sudah pakai aset asli dari folder aset/Icon level selesai/ (bukan emoji lagi),
dan sudah menerima data skor ASLI (bukan dummy 200/450/650), yang datang
dari logic/score_manager.py -> get_rincian_skor().

Dibuat sebagai class, mengikuti pola level_screen.py, supaya siap dipasang
di main.py.

Cara pakai dari game_screen.py / main.py nanti (kurang lebih):

    rincian = self.score_manager.get_rincian_skor()
    # rincian = {"skor_dasar": 200, "bonus_waktu": 450, "total_skor": 650}

    frame = LevelSelesaiScreen(
        parent,
        rincian_skor=rincian,
        on_level_berikutnya=fungsi_mulai_level_berikutnya,
        on_ulangi=fungsi_ulangi_level_ini,
        on_menu_utama=fungsi_kembali_ke_menu,
    )
    frame.pack(fill="both", expand=True)
"""

import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDER_ICON = os.path.join(BASE_DIR, "aset", "Icon level selesai")

BG_COLOR = "#F5F7FB"
PRIMARY_BLUE = "#1565D8"
TOTAL_BG = "#EAF2FF"
TEXT_MUTED = "gray"
BONUS_COLOR = "#D97706"


def _muat(nama_file, size=None):
    img = Image.open(os.path.join(FOLDER_ICON, nama_file))
    if size:
        img = img.resize(size)
    return ImageTk.PhotoImage(img)


class LevelSelesaiScreen(tk.Frame):
    def __init__(
        self,
        parent,
        rincian_skor,
        on_level_berikutnya=None,
        on_ulangi=None,
        on_menu_utama=None,
        ada_level_berikutnya=True,
    ):

        super().__init__(parent, bg=BG_COLOR)

        self.rincian_skor = rincian_skor
        self.on_level_berikutnya = on_level_berikutnya
        self.on_ulangi = on_ulangi
        self.on_menu_utama = on_menu_utama
        self.ada_level_berikutnya = ada_level_berikutnya

        self._muat_aset()
        self._build_konten()

    # ------------------------------------------------------------
    # ASET
    # ------------------------------------------------------------
    def _muat_aset(self):
        self.gambar_trophy = _muat("Gambar trophy.png", (140, 140))
        self.icon_skor = _muat("Icon skor.png", (22, 22))
        self.icon_waktu = _muat("Icon waktu.png", (22, 22))
        self.icon_berikutnya = _muat("Icon level berikutnya.png", (18, 18))
        self.icon_ulangi = _muat("Icon ulangi.png", (18, 18))
        self.icon_menu = _muat("Icon menu utama.png", (18, 18))

    # ------------------------------------------------------------
    # KONTEN
    # ------------------------------------------------------------
    def _build_konten(self):
        frame = tk.Frame(self, bg=BG_COLOR)
        frame.pack(expand=True, fill="both")

        # ===== TROFI (gambar asli, sudah termasuk bintang) =====
        label_trophy = tk.Label(frame, image=self.gambar_trophy, bg=BG_COLOR)
        label_trophy.image = self.gambar_trophy
        label_trophy.pack(pady=(30, 10))

        # ===== JUDUL =====
        tk.Label(
            frame, text="Level Selesai!", font=("Poppins", 22, "bold"),
            bg=BG_COLOR, fg=PRIMARY_BLUE,
        ).pack(pady=(10, 0))

        tk.Label(
            frame, text="Selamat! Kamu berhasil menyelesaikan level ini!",
            font=("Poppins", 9), bg=BG_COLOR, fg=TEXT_MUTED,
        ).pack(pady=(0, 20))

        # ===== CARD SKOR =====
        card = tk.Frame(frame, bg="white", bd=1, relief="solid")
        card.pack()

        skor_dasar = self.rincian_skor.get("skor_dasar", 0)
        bonus_waktu = self.rincian_skor.get("bonus_waktu", 0)
        total_skor = self.rincian_skor.get("total_skor", 0)

        # --- Skor Dasar ---
        row1 = tk.Frame(card, bg="white")
        row1.pack(fill="x", padx=20, pady=(15, 5))

        kiri1 = tk.Frame(row1, bg="white")
        kiri1.pack(side="left")
        tk.Label(kiri1, image=self.icon_skor, bg="white").pack(
            side="left", padx=(0, 6))
        tk.Label(kiri1, text="Skor Dasar", bg="white").pack(side="left")

        tk.Label(
            row1, text=str(skor_dasar), bg="white", font=("Poppins", 10, "bold"),
        ).pack(side="right")

        # --- Bonus Waktu ---
        row2 = tk.Frame(card, bg="white")
        row2.pack(fill="x", padx=20, pady=5)

        kiri2 = tk.Frame(row2, bg="white")
        kiri2.pack(side="left")
        tk.Label(kiri2, image=self.icon_waktu, bg="white").pack(
            side="left", padx=(0, 6))
        tk.Label(kiri2, text="Bonus Waktu", bg="white").pack(side="left")

        tk.Label(
            row2, text=f"+{bonus_waktu}", bg="white", fg=BONUS_COLOR,
            font=("Poppins", 10, "bold"),
        ).pack(side="right")

        ttk.Separator(card).pack(fill="x", padx=20, pady=10)

        # --- Total ---
        total = tk.Frame(card, bg=TOTAL_BG)
        total.pack(fill="x")

        tk.Label(
            total, text="TOTAL SKOR", bg=TOTAL_BG, fg=PRIMARY_BLUE,
            font=("Poppins", 10, "bold"),
        ).pack(pady=(8, 0))

        tk.Label(
            total, text=str(total_skor), bg=TOTAL_BG, fg=PRIMARY_BLUE,
            font=("Poppins", 24, "bold"),
        ).pack(pady=(0, 10))

        # ===== TOMBOL =====
        # CATATAN: width/height di bawah ini satuannya KARAKTER TEKS
        # (bukan pixel) karena tombol punya image+text sekaligus. Kalau
        # dikasih angka besar (mis. width=280) tombolnya jadi sangat lebar
        # dan ikonnya "terbuang" jauh ke kanan sampai keluar layar.
        if self.ada_level_berikutnya:
            btn_berikutnya = tk.Button(
                frame, text="  Level Berikutnya  ", image=self.icon_berikutnya,
                compound="right", bg=PRIMARY_BLUE, fg="white",
                font=("Poppins", 10, "bold"), relief="flat", cursor="hand2",
                padx=20, pady=10, command=self._klik_level_berikutnya,
            )
            btn_berikutnya.pack(pady=20, ipadx=60)

        bawah = tk.Frame(frame, bg=BG_COLOR)
        bawah.pack()

        tk.Button(
            bawah, text=" Ulangi", image=self.icon_ulangi, compound="left",
            bg="white", fg=PRIMARY_BLUE, relief="solid", bd=1,
            font=("Poppins", 9, "bold"), padx=12, pady=6, cursor="hand2",
            command=self._klik_ulangi,
        ).pack(side="left", padx=5)

        tk.Button(
            bawah, text=" Menu Utama", image=self.icon_menu, compound="left",
            bg="white", fg=PRIMARY_BLUE, relief="solid", bd=1,
            font=("Poppins", 9, "bold"), padx=12, pady=6, cursor="hand2",
            command=self._klik_menu_utama,
        ).pack(side="left", padx=5)

    # ------------------------------------------------------------
    # AKSI (tinggal manggil callback yang dikasih dari luar)
    # ------------------------------------------------------------
    def _klik_level_berikutnya(self):
        if self.on_level_berikutnya:
            self.on_level_berikutnya()

    def _klik_ulangi(self):
        if self.on_ulangi:
            self.on_ulangi()

    def _klik_menu_utama(self):
        if self.on_menu_utama:
            self.on_menu_utama()


# ------------------------------------------------------------
# MODE TES MANDIRI
# ------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Level Selesai")
    root.geometry("800x650")
    root.state("zoomed")  # fullscreen
    root.resizable(False, False)
    root.configure(bg=BG_COLOR)

    # contoh data, nanti ini datang dari score_manager.get_rincian_skor()
    contoh_rincian = {"skor_dasar": 200, "bonus_waktu": 450, "total_skor": 650}

    def kembali_ke_menu():
        # 1. tutup window Level Selesai yang sedang tampil
        root.destroy()
        # 2. buka menu_screen.py (dia punya root & mainloop sendiri)
        import menu_screen

    LevelSelesaiScreen(
        root,
        rincian_skor=contoh_rincian,
        on_level_berikutnya=lambda: print("klik: Level Berikutnya"),
        on_ulangi=lambda: print("klik: Ulangi"),
        on_menu_utama=kembali_ke_menu,
    ).pack(fill="both", expand=True)

    root.mainloop()
