import os
import tkinter as tk
from PIL import Image, ImageTk


class MenuScreen(tk.Frame):
    """Halaman Menu Utama - Color Ball Sort Puzzle."""

    def __init__(self, parent, on_mulai=None, on_leaderboard=None,
                 on_progress=None, on_setting=None, on_logout=None):
        super().__init__(parent, bg="#F5F7FB")

        # Callback dari main.py (kalau tidak diisi, aman/tidak error)
        self.on_mulai = on_mulai or (lambda: None)
        self.on_leaderboard = on_leaderboard or (lambda: None)
        self.on_progress = on_progress or (lambda: None)
        self.on_setting = on_setting or (lambda: None)
        self.on_logout = on_logout or (lambda: None)

        # ---------------------------------------
        # PATH ASSET
        # ---------------------------------------
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.folder_aset = os.path.join(base_dir, "aset")
        self.folder_icon = os.path.join(self.folder_aset, "Icon menu utama")

        self.muat_aset()
        self.buat_header()
        self.buat_sidebar()
        self.buat_konten()

    # ---------------------------------------
    # FUNGSI BANTU (HELPER)
    # ---------------------------------------

    def muat(self, path, size=None):
        """Buka gambar dari file dan ubah jadi PhotoImage, bisa resize."""
        img = Image.open(path)
        if size:
            img = img.resize(size)
        return ImageTk.PhotoImage(img)

    def hover_card(self, frame, masuk):
        """Ganti warna background card saat mouse masuk/keluar (efek hover)."""
        warna = "#F8FAFF" if masuk else "white"

        def ubah(widget):
            try:
                widget.configure(bg=warna)
            except tk.TclError:
                pass
            for anak in widget.winfo_children():
                ubah(anak)

        ubah(frame)

    def buat_card_klik(self, frame, command):
        """Bikin seluruh area card (termasuk isinya) bisa diklik."""
        frame.bind("<Button-1>", lambda e: command())
        frame.bind("<Enter>", lambda e: self.hover_card(frame, True))
        frame.bind("<Leave>", lambda e: self.hover_card(frame, False))
        frame.configure(cursor="hand2")
        for anak in frame.winfo_children():
            anak.bind("<Button-1>", lambda e: command())
            anak.configure(cursor="hand2")
            for cucu in anak.winfo_children():
                cucu.bind("<Button-1>", lambda e: command())
                cucu.configure(cursor="hand2")

    # ---------------------------------------
    # MUAT SEMUA ASSET GAMBAR
    # ---------------------------------------

    def muat_aset(self):
        self.logo = self.muat(os.path.join(self.folder_aset, "logo_baru.PNG"), (55, 55))
        self.icon_home = self.muat(os.path.join(self.folder_icon, "Icon home.png"))
        self.icon_trophy = self.muat(os.path.join(self.folder_icon, "Icon trophy.png"))
        self.icon_progress = self.muat(os.path.join(self.folder_icon, "Icon progress.png"))
        self.icon_keluar = self.muat(os.path.join(self.folder_icon, "Icon keluar.png"))
        self.gambar_trophy = self.muat(os.path.join(self.folder_icon, "Gambar trophy.png"), (60, 60))
        self.gambar_progress = self.muat(os.path.join(self.folder_icon, "Gambar progress.png"), (60, 60))
        self.icon_setting = self.muat(os.path.join(self.folder_icon, "Button setting.png"), (26, 26))
        self.icon_play = self.muat(os.path.join(self.folder_icon, "Icon play.png"), (40, 40))

    # ---------------------------------------
    # HEADER
    # ---------------------------------------

    def buat_header(self):
        header = tk.Frame(self, bg="#F5F7FB", height=80)
        header.pack(fill="x")

        tk.Label(header, image=self.logo, bg="#F5F7FB").pack(side="left", padx=(25, 10), pady=15)
        tk.Label(
            header, text="Color Ball Sort Puzzle", font=("Arial", 18, "bold"),
            bg="#F5F7FB", fg="#1565D8"
        ).pack(side="left")

        tk.Button(
            header, image=self.icon_setting, bg="#F5F7FB", relief="flat",
            cursor="hand2", command=self.on_setting
        ).pack(side="right", padx=30)

    # ---------------------------------------
    # SIDEBAR
    # ---------------------------------------

    def buat_sidebar(self):
        frame_utama = tk.Frame(self, bg="#F5F7FB")
        frame_utama.pack(fill="both", expand=True)
        self.frame_utama = frame_utama

        sidebar = tk.Frame(frame_utama, bg="white", width=230)
        sidebar.pack(side="left", fill="y", padx=(20, 10), pady=10)
        sidebar.pack_propagate(False)

        tk.Button(
            sidebar, text="  Beranda", image=self.icon_home, compound="left",
            font=("Arial", 11, "bold"), bg="#1565D8", fg="white",
            relief="flat", anchor="w", padx=20
        ).pack(fill="x", pady=(20, 8))

        tk.Button(
            sidebar, text="  Papan Peringkat", image=self.icon_trophy, compound="left",
            font=("Arial", 11), bg="white", fg="#333333", relief="flat",
            anchor="w", padx=20, cursor="hand2", command=self.on_leaderboard
        ).pack(fill="x", pady=8)

        tk.Button(
            sidebar, text="  Progress", image=self.icon_progress, compound="left",
            font=("Arial", 11), bg="white", fg="#333333", relief="flat",
            anchor="w", padx=20, cursor="hand2", command=self.on_progress
        ).pack(fill="x", pady=8)

        tk.Label(sidebar, bg="white").pack(expand=True)  # ruang kosong

        tk.Button(
            sidebar, text="  Keluar", image=self.icon_keluar, compound="left",
            font=("Arial", 11), bg="white", fg="#D32F2F", relief="flat",
            anchor="w", padx=20, cursor="hand2", command=self.on_logout
        ).pack(fill="x", pady=20)

    # ---------------------------------------
    # KONTEN KANAN (BANNER + CARD)
    # ---------------------------------------

    def buat_konten(self):
        konten = tk.Frame(self.frame_utama, bg="#F5F7FB")
        konten.pack(side="left", fill="both", expand=True, padx=15, pady=10)

        lebar_konten = 900  # lebar tetap banner & card, mengikuti proporsi UI

        # ---- Banner Mulai Game ----
        banner = tk.Frame(konten, bg="#1565D8", width=lebar_konten, height=180)
        banner.pack(anchor="w")
        banner.pack_propagate(False)
        banner.bind("<Button-1>", lambda e: self.on_mulai())
        banner.configure(cursor="hand2")

        label_badge = tk.Label(
            banner, text="  Mainkan Sekarang  ", bg="#4F8FF7", fg="white",
            font=("Arial", 9, "bold"), padx=6, pady=4
        )
        label_badge.place(x=30, y=25)

        label_judul = tk.Label(
            banner, text="Mulai Game", bg="#1565D8", fg="white",
            font=("Arial", 26, "bold")
        )
        label_judul.place(x=30, y=65)

        label_deskripsi = tk.Label(
            banner, text="Lanjutkan dari Level 12 dan cetak skor tertinggi.",
            bg="#1565D8", fg="white", font=("Arial", 10)
        )
        label_deskripsi.place(x=30, y=115)

        for widget in (label_badge, label_judul, label_deskripsi):
            widget.bind("<Button-1>", lambda e: self.on_mulai())
            widget.configure(cursor="hand2")

        tk.Button(
            banner, image=self.icon_play, bg="#1565D8", relief="flat", bd=0,
            activebackground="#1565D8", cursor="hand2", command=self.on_mulai
        ).place(relx=0.94, rely=0.5, anchor="center")

        # ---- Card menu (klik langsung tanpa tombol, sesuai UI) ----
        gap_card = 20
        lebar_card = (lebar_konten - gap_card) // 2

        card = tk.Frame(konten, bg="#F5F7FB", width=lebar_konten, height=180)
        card.pack(anchor="w", pady=20)
        card.pack_propagate(False)

        card1 = self.buat_card(
            card, lebar_card, self.gambar_trophy, "Papan Peringkat",
            "Lihat peringkatmu dibandingkan\ndengan teman-teman sekolah.",
            self.on_leaderboard
        )
        card1.pack(side="left", padx=(0, gap_card))

        card2 = self.buat_card(
            card, lebar_card, self.gambar_progress, "Progress Saya",
            "Pantau statistik permainan\ndan koleksi bola spesialmu.",
            self.on_progress
        )
        card2.pack(side="left")

    def buat_card(self, induk, lebar, gambar, judul, deskripsi, command):
        c = tk.Frame(induk, bg="white", bd=1, relief="solid", width=lebar, height=180)
        c.pack_propagate(False)
        isi = tk.Frame(c, bg="white")
        isi.pack(expand=True)  # bikin konten di dalam card rata tengah vertikal
        tk.Label(isi, image=gambar, bg="white").pack(pady=(0, 10))
        tk.Label(isi, text=judul, bg="white", font=("Arial", 13, "bold")).pack()
        tk.Label(isi, text=deskripsi, bg="white", fg="gray", justify="center").pack(pady=(5, 0))
        self.buat_card_klik(c, command)
        return c