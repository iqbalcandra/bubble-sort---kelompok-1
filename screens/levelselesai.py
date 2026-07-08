"""
screens/level_selesai_screen.py (atau nama file kamu: level_selesai.py)

Halaman "Level Selesai" — ditampilkan setelah pemain menyelesaikan sebuah level.

CATATAN PATH ASET:
Folder "Icon level selesai" ada di dalam folder "aset" di root project,
sama seperti pola folder "Icon papan peringkat" di leaderboard_screen.py.
Isinya:
    - Gambar trophy.png        -> ilustrasi bintang + piala di atas
    - Icon skor.png            -> icon kecil di baris "Skor Dasar"
    - Icon waktu.png           -> icon kecil di baris "Bonus Waktu"
    - Icon level berikutnya.png-> icon panah di tombol "Level Berikutnya"
    - Icon ulangi.png          -> icon reload di tombol "Ulangi"
    - Icon menu utama.png      -> icon menu di tombol "Menu Utama"

Kalau file ini kamu taruh BUKAN langsung di dalam folder "screens/"
(misalnya dipindah satu level), sesuaikan BASE_DIR di bawah.
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk

# ------------------------------------------------------------
# PATH ASET
# ------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDER_ICON = os.path.join(BASE_DIR, "aset", "Icon level selesai")

BG_COLOR = "#F5F7FB"
PRIMARY_BLUE = "#1565D8"
ORANGE = "#D97706"
TOTAL_BG = "#EAF2FF"
BORDER_COLOR = "#E5E5E5"

CARD_WIDTH = 430


def _muat(nama_file, size=None):
    from PIL import Image, ImageTk
    img = Image.open(os.path.join(FOLDER_ICON, nama_file))
    if size:
        img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)


def _kembali_ke_menu(parent):
    """Tutup window Level Selesai lalu buka menu_screen.py, sama pola
    dengan LeaderboardScreen.kembali() di leaderboard_screen.py."""
    root_window = parent.winfo_toplevel()
    root_window.destroy()

    menu_path = os.path.join(BASE_DIR, "screens", "menu_screen.py")
    subprocess.Popen([sys.executable, menu_path])


def level_selesai(parent, skor_dasar=200, bonus_waktu=450):
    # mengatur warna background halaman
    parent.configure(bg=BG_COLOR)

    # --------------------------------------------------------
    # LOAD ICON (disimpan sebagai atribut widget supaya tidak
    # kena garbage-collected oleh Tkinter)
    # --------------------------------------------------------
    icon_trophy = _muat("Gambar trophy.png", (140, 140))
    icon_skor = _muat("Icon skor.png", (16, 16))
    icon_waktu = _muat("Icon waktu.png", (16, 16))
    icon_next = _muat("Icon level berikutnya.png", (16, 16))
    icon_ulangi = _muat("Icon ulangi.png", (16, 16))
    icon_menu = _muat("Icon menu utama.png", (16, 16))

    frame = tk.Frame(parent, bg=BG_COLOR)
    frame.pack(expand=True, fill="both")

    # simpan referensi biar tidak hilang (anti garbage-collect)
    frame.image_refs = [
        icon_trophy, icon_skor, icon_waktu,
        icon_next, icon_ulangi, icon_menu,
    ]

    isi = tk.Frame(frame, bg=BG_COLOR)
    isi.pack(pady=40)

    # ================= ICON TROPHY + BINTANG =================
    tk.Label(
        isi, image=icon_trophy, bg=BG_COLOR,
    ).pack()

    # ================= JUDUL =================
    tk.Label(
        isi,
        text="Level Selesai!",
        font=("Poppins", 22, "bold"),
        bg=BG_COLOR,
        fg=PRIMARY_BLUE,
    ).pack(pady=(10, 0))

    tk.Label(
        isi,
        text="Selamat! Kamu berhasil menyelesaikan level ini!",
        font=("Poppins", 9),
        bg=BG_COLOR,
        fg="gray",
    ).pack(pady=(0, 20))

    # ================= CARD =================
    # frame pembungkus supaya lebar card konsisten (430px)
    card_wrap = tk.Frame(isi, bg=BG_COLOR, width=CARD_WIDTH)
    card_wrap.pack()
    card_wrap.pack_propagate(False)

    card = tk.Frame(
        card_wrap,
        bg="white",
        highlightbackground=BORDER_COLOR,
        highlightthickness=1,
    )
    card.pack(fill="both", expand=True)

    # ---- Skor Dasar ----
    row1 = tk.Frame(card, bg="white")
    row1.pack(fill="x", padx=20, pady=(15, 8))

    kiri1 = tk.Frame(row1, bg="white")
    kiri1.pack(side="left")
    tk.Label(kiri1, image=icon_skor, bg="white").pack(side="left", padx=(0, 6))
    tk.Label(kiri1, text="Skor Dasar", bg="white",
             font=("Poppins", 9)).pack(side="left")

    tk.Label(
        row1, text=str(skor_dasar), bg="white", font=("Poppins", 11, "bold"),
    ).pack(side="right")

    # ---- Bonus Waktu ----
    row2 = tk.Frame(card, bg="white")
    row2.pack(fill="x", padx=20, pady=(0, 15))

    kiri2 = tk.Frame(row2, bg="white")
    kiri2.pack(side="left")
    tk.Label(kiri2, image=icon_waktu, bg="white").pack(
        side="left", padx=(0, 6))
    tk.Label(kiri2, text="Bonus Waktu", bg="white",
             font=("Poppins", 9)).pack(side="left")

    tk.Label(
        row2, text=f"+{bonus_waktu}", bg="white", fg=ORANGE,
        font=("Poppins", 11, "bold"),
    ).pack(side="right")

    ttk.Separator(card).pack(fill="x", padx=20)

    # ---- Total ----
    total = tk.Frame(card, bg=TOTAL_BG)
    total.pack(fill="x")

    baris_total = tk.Frame(total, bg=TOTAL_BG)
    baris_total.pack(fill="x", padx=20, pady=12)

    tk.Label(
        baris_total, text="Total Skor", bg=TOTAL_BG, fg=PRIMARY_BLUE,
        font=("Poppins", 10, "bold"),
    ).pack(side="left")

    tk.Label(
        baris_total, text=str(skor_dasar + bonus_waktu), bg=TOTAL_BG,
        fg=PRIMARY_BLUE, font=("Poppins", 18, "bold"),
    ).pack(side="right")

    # ================= BUTTON =================
    tk.Button(
        isi,
        text="  Level Berikutnya",
        image=icon_next,
        compound="right",
        bg=PRIMARY_BLUE,
        fg="white",
        activebackground=PRIMARY_BLUE,
        activeforeground="white",
        font=("Poppins", 10, "bold"),
        relief="flat",
        bd=0,
        width=CARD_WIDTH - 20,
        pady=10,
        cursor="hand2",
    ).pack(pady=(20, 8))

    bawah = tk.Frame(isi, bg=BG_COLOR)
    bawah.pack()

    tk.Button(
        bawah,
        text=" Ulangi",
        image=icon_ulangi,
        compound="left",
        bg="white",
        fg=PRIMARY_BLUE,
        activeforeground=PRIMARY_BLUE,
        font=("Poppins", 9, "bold"),
        relief="solid",
        bd=1,
        highlightbackground=PRIMARY_BLUE,
        width=(CARD_WIDTH // 2) - 25,
        pady=8,
        cursor="hand2",
    ).pack(side="left", padx=(0, 6))

    tk.Button(
        bawah,
        text=" Menu Utama",
        image=icon_menu,
        compound="left",
        bg="white",
        fg=PRIMARY_BLUE,
        activeforeground=PRIMARY_BLUE,
        font=("Poppins", 9, "bold"),
        relief="solid",
        bd=1,
        highlightbackground=PRIMARY_BLUE,
        width=(CARD_WIDTH // 2) - 25,
        pady=8,
        cursor="hand2",
        command=lambda: _kembali_ke_menu(parent),
    ).pack(side="left", padx=(6, 0))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Level Selesai")
    root.geometry("800x650")

    level_selesai(root)

    root.mainloop()
