import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# ---------------------------------------
# FUNGSI AKSI
# ---------------------------------------

def mulai_game():
    messagebox.showinfo("Mulai Game", "Membuka halaman pemilihan level...")

def buka_leaderboard():
    messagebox.showinfo("Leaderboard", "Halaman leaderboard akan dibuka.")

def buka_progress():
    messagebox.showinfo("Progress", "Halaman progress akan dibuka.")

def buka_setting():
    messagebox.showinfo("Pengaturan", "Halaman pengaturan akan dibuka.")

def keluar():
    if messagebox.askyesno("Keluar", "Apakah Anda yakin ingin keluar?"):
        root.destroy()

def hover_card(frame, masuk):
    warna = "#F8FAFF" if masuk else "white"
    def ubah(f):
        try:
            f.configure(bg=warna)
        except tk.TclError:
            pass
        for c in f.winfo_children():
            ubah(c)
    ubah(frame)

def buat_card_klik(frame, command):
    frame.bind("<Button-1>", lambda e: command())
    frame.bind("<Enter>", lambda e: hover_card(frame, True))
    frame.bind("<Leave>", lambda e: hover_card(frame, False))
    frame.configure(cursor="hand2")
    for child in frame.winfo_children():
        child.bind("<Button-1>", lambda e: command())
        child.configure(cursor="hand2")
        for cucu in child.winfo_children():
            cucu.bind("<Button-1>", lambda e: command())
            cucu.configure(cursor="hand2")


# ---------------------------------------
# WINDOW
# ---------------------------------------

root = tk.Tk()
root.title("Color Ball Sort Puzzle")
root.geometry("1440x1024")
root.configure(bg="#F5F7FB")
root.resizable(False, False)

# ---------------------------------------
# PATH ASSET
# ---------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
folder_aset = os.path.join(BASE_DIR, "aset")
folder_icon = os.path.join(folder_aset, "Icon menu utama")

def muat(path, size=None):
    img = Image.open(path)
    if size:
        img = img.resize(size)
    return ImageTk.PhotoImage(img)

logo = muat(os.path.join(folder_aset, "logo_baru.PNG"), (55, 55))
icon_home = muat(os.path.join(folder_icon, "Icon home.png"))
icon_trophy = muat(os.path.join(folder_icon, "Icon trophy.png"))
icon_progress = muat(os.path.join(folder_icon, "Icon progress.png"))
icon_keluar = muat(os.path.join(folder_icon, "Icon keluar.png"))
gambar_trophy = muat(os.path.join(folder_icon, "Gambar trophy.png"), (60, 60))
gambar_progress = muat(os.path.join(folder_icon, "Gambar progress.png"), (60, 60))
icon_setting = muat(os.path.join(folder_icon, "Button setting.png"), (26, 26))
icon_play = muat(os.path.join(folder_icon, "Icon play.png"), (40, 40))

# ---------------------------------------
# HEADER
# ---------------------------------------

header = tk.Frame(root, bg="#F5F7FB", height=80)
header.pack(fill="x")

tk.Label(header, image=logo, bg="#F5F7FB").pack(side="left", padx=(25, 10), pady=15)
tk.Label(
    header, text="Color Ball Sort Puzzle", font=("Arial", 18, "bold"),
    bg="#F5F7FB", fg="#1565D8"
).pack(side="left")

tk.Button(
    header, image=icon_setting, bg="#F5F7FB", relief="flat",
    cursor="hand2", command=buka_setting
).pack(side="right", padx=30)

# ---------------------------------------
# FRAME UTAMA
# ---------------------------------------

frame_utama = tk.Frame(root, bg="#F5F7FB")
frame_utama.pack(fill="both", expand=True)

# ---------------------------------------
# SIDEBAR
# ---------------------------------------

sidebar = tk.Frame(frame_utama, bg="white", width=230)
sidebar.pack(side="left", fill="y", padx=(20, 10), pady=10)
sidebar.pack_propagate(False)

tk.Button(
    sidebar, text="  Beranda", image=icon_home, compound="left",
    font=("Arial", 11, "bold"), bg="#1565D8", fg="white",
    relief="flat", anchor="w", padx=20
).pack(fill="x", pady=(20, 8))

tk.Button(
    sidebar, text="  Papan Peringkat", image=icon_trophy, compound="left",
    font=("Arial", 11), bg="white", fg="#333333", relief="flat",
    anchor="w", padx=20, cursor="hand2", command=buka_leaderboard
).pack(fill="x", pady=8)

tk.Button(
    sidebar, text="  Progress", image=icon_progress, compound="left",
    font=("Arial", 11), bg="white", fg="#333333", relief="flat",
    anchor="w", padx=20, cursor="hand2", command=buka_progress
).pack(fill="x", pady=8)

tk.Label(sidebar, bg="white").pack(expand=True)  # ruang kosong

tk.Button(
    sidebar, text="  Keluar", image=icon_keluar, compound="left",
    font=("Arial", 11), bg="white", fg="#D32F2F", relief="flat",
    anchor="w", padx=20, cursor="hand2", command=keluar
).pack(fill="x", pady=20)

# ---------------------------------------
# KONTEN KANAN
# ---------------------------------------

konten = tk.Frame(frame_utama, bg="#F5F7FB")
konten.pack(side="left", fill="both", expand=True, padx=15, pady=10)

LEBAR_KONTEN = 900  # lebar tetap banner & card, mengikuti proporsi UI (tidak melebar penuh)

# ---- Banner Mulai Game ----

banner = tk.Frame(konten, bg="#1565D8", width=LEBAR_KONTEN, height=180)
banner.pack(anchor="w")
banner.pack_propagate(False)

tk.Label(
    banner, text="  Mainkan Sekarang  ", bg="#4F8FF7", fg="white",
    font=("Arial", 9, "bold"), padx=6, pady=4
).place(x=30, y=25)

tk.Label(
    banner, text="Mulai Game", bg="#1565D8", fg="white",
    font=("Arial", 26, "bold")
).place(x=30, y=65)

tk.Label(
    banner, text="Lanjutkan dari Level 12 dan cetak skor tertinggi.",
    bg="#1565D8", fg="white", font=("Arial", 10)
).place(x=30, y=115)

tk.Button(
    banner, image=icon_play, bg="#1565D8", relief="flat", bd=0,
    activebackground="#1565D8", cursor="hand2", command=mulai_game
).place(relx=0.94, rely=0.5, anchor="center")

# ---- Card menu (klik langsung tanpa tombol, sesuai UI) ----

GAP_CARD = 20
LEBAR_CARD = (LEBAR_KONTEN - GAP_CARD) // 2

card = tk.Frame(konten, bg="#F5F7FB", width=LEBAR_KONTEN, height=180)
card.pack(anchor="w", pady=20)
card.pack_propagate(False)

def buat_card(induk, gambar, judul, deskripsi, command):
    c = tk.Frame(induk, bg="white", bd=1, relief="solid", width=LEBAR_CARD, height=180)
    c.pack_propagate(False)
    isi = tk.Frame(c, bg="white")
    isi.pack(expand=True)  # bikin konten di dalam card jadi rata tengah vertikal
    tk.Label(isi, image=gambar, bg="white").pack(pady=(0, 10))
    tk.Label(isi, text=judul, bg="white", font=("Arial", 13, "bold")).pack()
    tk.Label(isi, text=deskripsi, bg="white", fg="gray", justify="center").pack(pady=(5, 0))
    buat_card_klik(c, command)
    return c

card1 = buat_card(
    card, gambar_trophy, "Papan Peringkat",
    "Lihat peringkatmu dibandingkan\ndengan teman-teman sekolah.",
    buka_leaderboard
)
card1.pack(side="left", padx=(0, GAP_CARD))

card2 = buat_card(
    card, gambar_progress, "Progress Saya",
    "Pantau statistik permainan\ndan koleksi bola spesialmu.",
    buka_progress
)
card2.pack(side="left")

# ---------------------------------------
# MENJALANKAN PROGRAM
# ---------------------------------------

root.mainloop()