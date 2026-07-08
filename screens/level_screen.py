"""
screens/level_screen.py
"""

import os
import tkinter as tk

from logic.level_manager import LevelManager
from logic.progres_manager import ProgressManager
from theme import BG_COLOR, CARD_COLOR, PRIMARY_BLUE, TEXT_DARK, TEXT_MUTED, LEVEL_BADGE_COLOR


_ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
ASSET_MENU_DIR = os.path.join(_ROOT_DIR, "aset", "Icon menu utama")
ASSET_LOGIN_DIR = os.path.join(_ROOT_DIR, "aset", "Icon Login")


def _load_icon(folder, nama_file):
    path = os.path.join(folder, nama_file)
    try:
        return tk.PhotoImage(file=path)
    except Exception as e:
        print(f"[WARNING] Gagal load icon '{nama_file}': {e}")
        return None


DESKRIPSI_LEVEL = {
    "Mudah": "Cocok untuk memulai petualangan pertamamu. Santai dan menyenangkan!",
    "Sedang": "Butuh sedikit konsentrasi lebih untuk memilah semua bola berwarna.",
    "Sulit": "Hanya untuk para ahli! Banyak bola dan tabung yang menantang otak.",
}

LEVEL_STYLE = {
    "Mudah": {"badge_bg": "#DCEBFB", "accent": "#1565C0"},
    "Sedang": {"badge_bg": "#FBE7D1", "accent": "#8B4A12"},
    "Sulit": {"badge_bg": "#FADCDC", "accent": "#C62828"},
}
STYLE_DEFAULT = {"badge_bg": "#E4E4E4", "accent": PRIMARY_BLUE}

WARNA_ABU_TERKUNCI = "#D9D9D9"
TEKS_ABU_TERKUNCI = "#9A9A9A"

SIDEBAR_BG = "#FFFFFF"
SIDEBAR_WIDTH = 230
NAV_AKTIF_BG = PRIMARY_BLUE


class LevelScreen(tk.Frame):
    def __init__(
        self,
        parent,
        user_data,
        on_pilih_level=None,
        on_kembali=None,
        on_papan_peringkat=None,
        on_progress=None,
        on_keluar=None,
    ):
        super().__init__(parent, bg=BG_COLOR)

        self.user_data = user_data
        self.on_pilih_level = on_pilih_level
        self.on_kembali = on_kembali
        self.on_papan_peringkat = on_papan_peringkat
        self.on_progress = on_progress
        self.on_keluar = on_keluar

        self.level_manager = LevelManager()
        self.progres_manager = ProgressManager()

        self._load_icons()
        self._muat_data()

        self._build_layout()

    def _load_icons(self):
        self.icon_home = _load_icon(ASSET_MENU_DIR, "Icon home.png")
        self.icon_trophy = _load_icon(ASSET_MENU_DIR, "Icon trophy.png")
        self.icon_progress = _load_icon(ASSET_MENU_DIR, "Icon progress.png")
        self.icon_keluar = _load_icon(ASSET_MENU_DIR, "Icon keluar.png")
        self.icon_user = _load_icon(ASSET_LOGIN_DIR, "Icon user.png")

    def _muat_data(self):
        self.semua_level = self.level_manager.get_semua_level()

        progres = self.progres_manager.get_progress_pemain(
            self.user_data["id"])
        self.current_level_pemain = progres["current_level"] if progres else "Mudah"

    def _build_layout(self):
        main = tk.Frame(self, bg=BG_COLOR)
        main.pack(fill="both", expand=True)

        self._build_sidebar(main)

        content = tk.Frame(main, bg=BG_COLOR)
        content.pack(side="left", fill="both", expand=True)

        self._build_konten(content)

    def _build_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=SIDEBAR_BG, width=SIDEBAR_WIDTH)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        profil = tk.Frame(sidebar, bg=SIDEBAR_BG)
        profil.pack(fill="x", padx=20, pady=(25, 20))

        if self.icon_user:
            avatar = tk.Label(
                profil, image=self.icon_user, bg="#EAF2FF", bd=1, relief="solid"
            )
        else:
            avatar = tk.Label(
                profil, text="\U0001F464", font=("Arial", 18), bg="#EAF2FF",
                width=2, height=1, bd=1, relief="solid",
            )
        avatar.pack(side="left")

        info = tk.Frame(profil, bg=SIDEBAR_BG)
        info.pack(side="left", padx=(10, 0))

        nama_pemain = self.user_data.get("username", "Pemain")
        level_akun = self.user_data.get("level", 1)

        tk.Label(
            info, text=nama_pemain, font=("Arial", 10, "bold"),
            bg=SIDEBAR_BG, fg=PRIMARY_BLUE,
        ).pack(anchor="w")

        tk.Label(
            info, text=f"Level {level_akun}", font=("Arial", 8),
            bg=SIDEBAR_BG, fg=TEXT_MUTED,
        ).pack(anchor="w")

        nav = tk.Frame(sidebar, bg=SIDEBAR_BG)
        nav.pack(fill="x", padx=14, pady=(10, 0))

        keluar_frame = tk.Frame(sidebar, bg=SIDEBAR_BG)
        keluar_frame.pack(side="bottom", fill="x", padx=14, pady=25)

        tk.Button(
            keluar_frame, text=" Keluar", image=self.icon_keluar, compound="left",
            font=("Arial", 10, "bold"), bg=SIDEBAR_BG, fg="#E53935",
            relief="flat", anchor="w", command=self._klik_keluar,
        ).pack(fill="x")

    def _build_nav_item(self, parent, icon, label, aktif, command):
        bg = NAV_AKTIF_BG if aktif else SIDEBAR_BG
        fg = "white" if aktif else TEXT_DARK

        btn = tk.Button(
            parent, text=f" {label}", image=icon, compound="left",
            font=("Arial", 10, "bold"), bg=bg, fg=fg,
            relief="flat", anchor="w", padx=10, pady=8,
            activebackground=bg,
            command=command if command else (lambda: None),
        )
        btn.pack(fill="x", pady=3)
        return btn

    def _build_konten(self, parent):
        tk.Label(
            parent, text="Pilih Tingkat Kesulitan", font=("Arial", 26, "bold"),
            bg=BG_COLOR, fg=TEXT_DARK,
        ).pack(pady=(50, 4))

        tk.Label(
            parent, text="Tentukan tantanganmu hari ini dan mulailah bermain!",
            font=("Arial", 11), bg=BG_COLOR, fg=TEXT_MUTED,
        ).pack(pady=(0, 30))

        area_card = tk.Frame(parent, bg=BG_COLOR)
        area_card.pack()

        for level_data in self.semua_level:
            terbuka = self.level_manager.is_level_terbuka(
                level_data["id_level"], self.current_level_pemain
            )
            self._build_card_level(area_card, level_data, terbuka)

    def _build_card_level(self, parent, level_data, terbuka: bool):
        nama_level = level_data["nama_level"]
        id_level = level_data["id_level"]

        gaya = LEVEL_STYLE.get(nama_level, STYLE_DEFAULT)
        badge_bg = gaya["badge_bg"] if terbuka else "#EDEDED"
        aksen = gaya["accent"] if terbuka else TEKS_ABU_TERKUNCI
        warna_teks = TEXT_DARK if terbuka else TEKS_ABU_TERKUNCI

        card = tk.Frame(
            parent, bg=CARD_COLOR,
            highlightbackground="#E5E5E5" if terbuka else WARNA_ABU_TERKUNCI,
            highlightthickness=1, width=280, height=380,
        )
        card.pack(side="left", padx=16)
        card.pack_propagate(False)

        canvas_icon = tk.Canvas(card, width=80, height=80,
                                bg=CARD_COLOR, highlightthickness=0)
        canvas_icon.pack(pady=(30, 10))
        canvas_icon.create_oval(
            5, 5, 75, 75, fill=aksen if terbuka else "#EDEDED", outline="")

        if terbuka:
            bintang = "\u2605" * id_level
            canvas_icon.create_text(
                35, 35, text=bintang, font=("Arial", 13), fill=aksen)
        else:
            canvas_icon.create_text(
                40, 40, text="\U0001F512", font=("Arial", 20))

        tk.Label(
            card, text=f"TINGKAT {id_level}", font=("Arial", 8, "bold"),
            bg=badge_bg, fg=aksen if terbuka else TEKS_ABU_TERKUNCI,
            padx=10, pady=3,
        ).pack(pady=(0, 10))

        tk.Label(
            card, text=nama_level, font=("Arial", 18, "bold"),
            bg=CARD_COLOR, fg=warna_teks,
        ).pack()

        deskripsi = DESKRIPSI_LEVEL.get(nama_level, "")
        tk.Label(
            card, text=deskripsi, font=("Arial", 9), bg=CARD_COLOR,
            fg=warna_teks, wraplength=230, justify="center",
        ).pack(pady=(8, 20), padx=16)

        if terbuka:
            tk.Button(
                card, text=f"Pilih {nama_level}", font=("Arial", 11, "bold"),
                bg=aksen, fg="white", relief="flat", width=18, pady=8,
                activebackground=aksen,
                command=lambda ld=level_data: self._klik_pilih_level(ld),
            ).pack(side="bottom", pady=20)
        else:
            tk.Button(
                card, text="\U0001F512 Terkunci", font=("Arial", 11, "bold"),
                bg="#EDEDED", fg=TEKS_ABU_TERKUNCI, relief="flat", width=18, pady=8,
                state="disabled",
            ).pack(side="bottom", pady=20)

    def _klik_pilih_level(self, level_data):
        if self.on_pilih_level:
            self.on_pilih_level(level_data)

    def _klik_papan_peringkat(self):
        if self.on_papan_peringkat:
            self.on_papan_peringkat()

    def _klik_progress(self):
        if self.on_progress:
            self.on_progress()

    def _klik_keluar(self):
        if self.on_keluar:
            self.on_keluar()
        elif self.on_kembali:
            self.on_kembali()
