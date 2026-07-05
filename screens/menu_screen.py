import tkinter as tk
from tkinter import messagebox

# import gamescreen
# import leaderboardscreen
# import progresscreen


# tombol play di banner biru -> mulai/lanjut main game
def mulai_game():
    messagebox.showinfo("Mulai Game", "Melanjutkan dari Level 12...")


# nav "Papan Peringkat" & card Papan Peringkat -> buka halaman leaderboard
def buka_leaderboard():
    root.destroy()
    # leaderboard_root = tk.Tk()
    # leaderboardscreen.LeaderboardScreen(leaderboard_root)
    # leaderboard_root.mainloop()


# nav "Prestasi" & card Progres Saya -> buka halaman statistik/progres
def buka_progres():
    messagebox.showinfo("Progres Saya", "Menampilkan statistik permainan...")


# tombol Keluar (sidebar / bar pink) -> minta konfirmasi dulu sebelum nutup app
def keluar():
    if messagebox.askyesno("Keluar", "Yakin mau keluar dari game?"):
        root.destroy()


root = tk.Tk()
root.title("Color Ball Sort Puzzle")
root.geometry("1000x650")
root.resizable(False, False)
root.configure(bg="#f9f9ff")

# ===========================
# Header atas
# ===========================
header = tk.Frame(root, bg="#f9f9ff")
header.pack(fill="x", pady=15)

logo = tk.Canvas(header, width=48, height=48, bg="#f9f9ff", highlightthickness=0)
logo.create_oval(2, 2, 46, 46, fill="#2170e4", outline="")
logo.create_text(24, 24, text="CB", fill="white", font=("Arial", 11, "bold"))
logo.pack(side="left", padx=20)

tk.Label(header, text="Color Ball Sort Puzzle", font=("Arial", 16, "bold"),
         bg="#f9f9ff", fg="#191b23").pack(side="left")

tk.Label(header, text="⚙", font=("Arial", 14), bg="#f9f9ff",
         fg="#2170e4").pack(side="right", padx=25)

# ===========================
# Sidebar kiri
# ===========================
sidebar = tk.Frame(root, bg="#f9f9ff", width=210, height=560)
sidebar.pack(side="left", fill="y", padx=(15, 0))

tk.Button(sidebar, text="🏠  Beranda", font=("Arial", 10, "bold"), bg="#2170e4",
          fg="white", relief="flat", anchor="w", padx=15
          ).pack(fill="x", pady=(10, 5))

tk.Button(sidebar, text="🏆  Papan Peringkat", font=("Arial", 10), bg="#f9f9ff",
          fg="#333", relief="flat", anchor="w", padx=15, command=buka_leaderboard
          ).pack(fill="x", pady=5)

tk.Button(sidebar, text="🎖  Prestasi", font=("Arial", 10), bg="#f9f9ff",
          fg="#333", relief="flat", anchor="w", padx=15, command=buka_progres
          ).pack(fill="x", pady=5)

tk.Button(sidebar, text="↪  Keluar", font=("Arial", 10), bg="#f9f9ff",
          fg="#ba1a1a", relief="flat", anchor="w", padx=15, command=keluar
          ).pack(fill="x", side="bottom", pady=20)

# ===========================
# Konten utama (kanan sidebar)
# ===========================
konten = tk.Frame(root, bg="#f9f9ff")
konten.pack(side="left", fill="both", expand=True, padx=20, pady=10)

# banner biru - mulai game
banner = tk.Frame(konten, bg="#2170e4")
banner.pack(fill="x", pady=(10, 20), ipady=20)

tk.Label(banner, text="Mainkan Sekarang", font=("Arial", 8, "bold"), bg="#4a8dec",
         fg="white", padx=10, pady=3).place(x=25, y=15)

isi_banner = tk.Frame(banner, bg="#2170e4")
isi_banner.place(x=25, y=45)
tk.Label(isi_banner, text="Mulai Game", font=("Arial", 20, "bold"),
         bg="#2170e4", fg="white").pack(side="left")
tk.Button(isi_banner, text="▶", font=("Arial", 12, "bold"), bg="white",
          fg="#2170e4", relief="flat", width=2, command=mulai_game
          ).pack(side="left", padx=15)

tk.Label(banner, text="Lanjutkan dari Level 12 dan cetak skor tertinggi.",
         font=("Arial", 9), bg="#2170e4", fg="#dce7fb").place(x=25, y=85)

banner.configure(height=140)

# dua card menu
card_area = tk.Frame(konten, bg="#f9f9ff")
card_area.pack(fill="x")

card_lb = tk.Frame(card_area, bg="white", bd=1, relief="solid", width=360, height=160)
card_lb.pack(side="left", padx=(0, 15))
card_lb.pack_propagate(False)

tk.Frame(card_lb, bg="#ffdcc6", width=50, height=50).place(x=20, y=20)
tk.Label(card_lb, text="🏆", bg="#ffdcc6", font=("Arial", 16)).place(x=35, y=32)
tk.Label(card_lb, text="Papan Peringkat", font=("Arial", 12, "bold"),
         bg="white", fg="#191b23").place(x=20, y=85)
tk.Label(card_lb, text="Lihat peringkatmu dibandingkan\ndengan teman-teman sekolah.",
         font=("Arial", 9), bg="white", fg="#5d5f5f", justify="left"
         ).place(x=20, y=110)
card_lb.bind("<Button-1>", lambda e: buka_leaderboard())

card_progres = tk.Frame(card_area, bg="white", bd=1, relief="solid", width=360, height=160)
card_progres.pack(side="left")
card_progres.pack_propagate(False)

tk.Frame(card_progres, bg="#e2e2e2", width=50, height=50).place(x=20, y=20)
tk.Label(card_progres, text="📊", bg="#e2e2e2", font=("Arial", 16)).place(x=33, y=32)
tk.Label(card_progres, text="Progres Saya", font=("Arial", 12, "bold"),
         bg="white", fg="#191b23").place(x=20, y=85)
tk.Label(card_progres, text="Pantau statistik permainan dan\nkoleksi bola spesialmu.",
         font=("Arial", 9), bg="white", fg="#5d5f5f", justify="left"
         ).place(x=20, y=110)
card_progres.bind("<Button-1>", lambda e: buka_progres())

# bar pink keluar
tk.Button(konten, text="↪  Keluar Permainan", font=("Arial", 10, "bold"),
          bg="#ffdad6", fg="#ba1a1a", relief="flat", command=keluar
          ).pack(fill="x", pady=20, ipady=10)

# footer kecil
tk.Label(root, text="Versi Desktop 1.0.4 • 2024 Studio Edukasi", font=("Arial", 8),
         bg="#f9f9ff", fg="#9a9a9a").place(x=790, y=625)

root.mainloop()