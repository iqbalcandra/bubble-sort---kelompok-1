import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDER_ICON = os.path.join(BASE_DIR, "aset", "Icon level selesai")

# Warna yang digunakan pada halaman
BG_COLOR = "#F5F7FB"
PRIMARY_BLUE = "#1565D8"
ORANGE = "#D97706"
TOTAL_BG = "#EAF2FF"
BORDER_COLOR = "#E5E5E5"

# Lebar card informasi skor
CARD_WIDTH = 430

# Memuat gambar dari folder aset
def muat(nama_file, size=None):
    img = Image.open(os.path.join(FOLDER_ICON, nama_file))
    if size:
        img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)


class LevelSelesaiScreen(tk.Frame):

    def __init__(
        self,
        parent,
        skor_dasar=200,
        bonus_waktu=450,
        on_level_berikutnya=None,
        on_ulangi=None,
        on_kembali=None,
    ):
        super().__init__(parent, bg=BG_COLOR)

        # Menyimpan nilai skor level
        self.skor_dasar = skor_dasar
        self.bonus_waktu = bonus_waktu

        # Callback dijalankan saat tombol dipilih
        self.on_level_berikutnya = on_level_berikutnya or (lambda: None)
        self.on_ulangi = on_ulangi or (lambda: None)
        self.on_kembali = on_kembali or (lambda: None)

        # Menampilkan halaman level selesai
        self.muat_aset()
        self.buat_konten()

    # ---------------------------------------
    # ASET
    # ---------------------------------------

    # Memuat gambar/icon yang digunakan pada halaman ini
    def muat_aset(self):
        self.icon_trophy = muat("Gambar trophy.png", (140, 140))
        self.icon_skor = muat("Icon skor.png", (16, 16))
        self.icon_waktu = muat("Icon waktu.png", (16, 16))
        self.icon_next = muat("Icon level berikutnya.png", (16, 16))
        self.icon_ulangi = muat("Icon ulangi.png", (16, 16))
        self.icon_menu = muat("Icon menu utama.png", (16, 16))

    # ---------------------------------------
    # KONTEN
    # ---------------------------------------

    # Menampilkan icon trophy, judul, card skor, dan tombol
    def buat_konten(self):
        
        # Frame utama halaman
        isi = tk.Frame(self, bg=BG_COLOR)
        isi.pack(pady=40)

        # Icon trophy + bintang
        tk.Label(isi, image=self.icon_trophy, bg=BG_COLOR).pack()

        # Judul
        tk.Label(
            isi, text="Level Selesai!", font=("Poppins", 22, "bold"),
            bg=BG_COLOR, fg=PRIMARY_BLUE,
        ).pack(pady=(10, 0))

        tk.Label(
            isi, text="Selamat! Kamu berhasil menyelesaikan level ini!",
            font=("Poppins", 9), bg=BG_COLOR, fg="gray",
        ).pack(pady=(0, 20))

        self.buat_card_skor(isi)
        self.buat_tombol(isi)

    # ---------------------------------------
    # CARD SKOR
    # ---------------------------------------

    # Menampilkan rincian skor dasar, bonus waktu, dan total skor
    def buat_card_skor(self, isi):

        # Menentukan lebar card agar tetap rapi
        card_wrap = tk.Frame(isi, bg=BG_COLOR, width=CARD_WIDTH)
        card_wrap.pack()
        card_wrap.pack_propagate(False)

        # Card untuk menampilkan informasi skor
        card = tk.Frame(
            card_wrap, bg="white",
            highlightbackground=BORDER_COLOR, highlightthickness=1,
        )
        card.pack(fill="both", expand=True)

        # Baris skor dasar
        row1 = tk.Frame(card, bg="white")
        row1.pack(fill="x", padx=20, pady=(15, 8))

        kiri1 = tk.Frame(row1, bg="white")
        kiri1.pack(side="left")
        tk.Label(kiri1, image=self.icon_skor, bg="white").pack(side="left", padx=(0, 6))
        tk.Label(kiri1, text="Skor Dasar", bg="white", font=("Poppins", 9)).pack(side="left")

        tk.Label(
            row1, text=str(self.skor_dasar), bg="white", font=("Poppins", 11, "bold"),
        ).pack(side="right")

        # Baris bonus waktu
        row2 = tk.Frame(card, bg="white")
        row2.pack(fill="x", padx=20, pady=(0, 15))

        kiri2 = tk.Frame(row2, bg="white")
        kiri2.pack(side="left")
        tk.Label(kiri2, image=self.icon_waktu, bg="white").pack(side="left", padx=(0, 6))
        tk.Label(kiri2, text="Bonus Waktu", bg="white", font=("Poppins", 9)).pack(side="left")

        tk.Label(
            row2, text=f"+{self.bonus_waktu}", bg="white", fg=ORANGE,
            font=("Poppins", 11, "bold"),
        ).pack(side="right")

        # Garis pemisah
        ttk.Separator(card).pack(fill="x", padx=20)

        # Bagian total skor
        total = tk.Frame(card, bg=TOTAL_BG)
        total.pack(fill="x")

        baris_total = tk.Frame(total, bg=TOTAL_BG)
        baris_total.pack(fill="x", padx=20, pady=12)

        tk.Label(
            baris_total, text="Total Skor", bg=TOTAL_BG, fg=PRIMARY_BLUE,
            font=("Poppins", 10, "bold"),
        ).pack(side="left")

        tk.Label(
            baris_total, text=str(self.skor_dasar + self.bonus_waktu), bg=TOTAL_BG,
            fg=PRIMARY_BLUE, font=("Poppins", 18, "bold"),
        ).pack(side="right")

    # ---------------------------------------
    # TOMBOL
    # ---------------------------------------

    # Menampilkan tombol Level Berikutnya, Ulangi, dan Menu Utama
    def buat_tombol(self, isi):
        # Tombol level berikutnya
        tk.Button(
            isi, text="  Level Berikutnya", image=self.icon_next, compound="right",
            bg=PRIMARY_BLUE, fg="white", activebackground=PRIMARY_BLUE,
            activeforeground="white", font=("Poppins", 10, "bold"), relief="flat",
            bd=0, width=CARD_WIDTH - 20, pady=10, cursor="hand2",
            command=self.klik_level_berikutnya,
        ).pack(pady=(20, 8))

        # Frame untuk tombol ulangi dan menu utama
        bawah = tk.Frame(isi, bg=BG_COLOR)
        bawah.pack()

        # Tombol ulangi
        tk.Button(
            bawah, text=" Ulangi", image=self.icon_ulangi, compound="left",
            bg="white", fg=PRIMARY_BLUE, activeforeground=PRIMARY_BLUE,
            font=("Poppins", 9, "bold"), relief="solid", bd=1,
            highlightbackground=PRIMARY_BLUE, width=(CARD_WIDTH // 2) - 25,
            pady=8, cursor="hand2", command=self.klik_ulangi,
        ).pack(side="left", padx=(0, 6))

        # Tombol menu utama
        tk.Button(
            bawah, text=" Menu Utama", image=self.icon_menu, compound="left",
            bg="white", fg=PRIMARY_BLUE, activeforeground=PRIMARY_BLUE,
            font=("Poppins", 9, "bold"), relief="solid", bd=1,
            highlightbackground=PRIMARY_BLUE, width=(CARD_WIDTH // 2) - 25,
            pady=8, cursor="hand2", command=self.klik_kembali,
        ).pack(side="left", padx=(6, 0))

    # ---------------------------------------
    # AKSI
    # ---------------------------------------

    # Lanjut ke level berikutnya
    def klik_level_berikutnya(self):
        self.on_level_berikutnya()

    # Ulangi level yang sama
    def klik_ulangi(self):
        self.on_ulangi()

    # Kembali ke menu utama
    def klik_kembali(self):
        self.on_kembali()