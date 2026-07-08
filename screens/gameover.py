import os
import tkinter as tk
from PIL import Image, ImageTk


class GameOverScreen(tk.Frame):

    def __init__(self, parent, on_retry=None, on_menu=None):
        super().__init__(parent, bg="#FDECEC")

        # Callback dijalankan saat tombol dipilih
        self.on_retry = on_retry or (lambda: None)
        self.on_menu = on_menu or (lambda: None)

        # Menentukan lokasi folder icon Game Over
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        folder = os.path.join(
            base_dir,
            "aset",
            "Icon permainan berakhir"
        )

        # Memuat gambar dan icon yang digunakan
        self.gambar_over = self.muat(
            os.path.join(folder, "Gambar berakhir.png"),
            (85, 85)
        )

        self.icon_retry = self.muat(
            os.path.join(folder, "Icon coba lagi.png"),
            (18, 18)
        )

        self.icon_home = self.muat(
            os.path.join(folder, "Icon home.png"),
            (18, 18)
        )

        self.icon_waktu = self.muat(
            os.path.join(folder, "Icon waktu habis.png"),
            (15, 15)
        )

        # Menampilkan halaman Game Over
        self.buat_tampilan()

    # Memuat gambar dari folder aset
    def muat(self, path, size=None):
        gambar = Image.open(path)
        if size:
            gambar = gambar.resize(size)
        return ImageTk.PhotoImage(gambar)

    # ---------------------------------------
    # TAMPILAN GAME OVER
    # ---------------------------------------

    # Menampilkan seluruh komponen halaman Game Over
    def buat_tampilan(self):

        # Card utama
        card = tk.Frame(
            self,
            bg="white",
            bd=1,
            relief="solid",
            width=560,
            height=460
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        card.pack_propagate(False)

        # Gambar game over
        tk.Label(
            card,
            image=self.gambar_over,
            bg="white"
        ).pack(pady=(30, 12))

        # Judul halaman
        tk.Label(
            card,
            text="Permainan Berakhir!",
            font=("Arial", 28, "bold"),
            bg="white",
            fg="#222222"
        ).pack()

        # Badge informasi waktu habis
        badge = tk.Frame(
            card,
            bg="#FFE2E2"
        )

        badge.pack(
            pady=20,
            ipadx=5
        )

        tk.Label(
            badge,
            image=self.icon_waktu,
            bg="#FFE2E2"
        ).pack(
            side="left",
            padx=(8, 4)
        )

        tk.Label(
            badge,
            text="Waktu habis! Anda gagal menyelesaikan level.",
            font=("Arial", 9),
            bg="#FFE2E2",
            fg="#D32F2F"
        ).pack(
            side="left",
            padx=(0, 8),
            pady=5
        )

        # Tombol mengulang permainan
        tk.Button(
            card,
            image=self.icon_retry,
            compound="left",
            text="  Coba Lagi",
            font=("Arial", 11, "bold"),
            bg="#1565D8",
            fg="white",
            activebackground="#1565D8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.on_retry
        ).pack(
            fill="x",
            padx=55,
            pady=(10, 12),
            ipady=10
        )

        # Tombol kembali ke menu utama
        tk.Button(
            card,
            image=self.icon_home,
            compound="left",
            text="  Kembali ke Menu",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#1565D8",
            activebackground="white",
            activeforeground="#1565D8",
            relief="solid",
            bd=1,
            cursor="hand2",
            command=self.on_menu
        ).pack(
            fill="x",
            padx=55,
            ipady=10
        )