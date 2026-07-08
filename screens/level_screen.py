"""
screens/level_screen.py

Halaman "Pilih Tingkat Kesulitan" - menampilkan 3 card level (Mudah/Sedang/
Sulit) sesuai desain Figma. Level ditampilkan DINAMIS dari database (bukan
hardcode 3 card), supaya kalau nanti ditambah level baru di tabel `levels`,
halaman ini otomatis menyesuaikan tanpa perlu ubah kode.

Status lock/unlock dihitung dari logic/level_manager.py (is_level_terbuka),
berdasarkan current_level yang tersimpan di progress pemain.
"""

import tkinter as tk

from logic.level_manager import LevelManager
from logic.progres_manager import ProgressManager
from theme import BG_COLOR, CARD_COLOR, PRIMARY_BLUE, TEXT_DARK, TEXT_MUTED, LEVEL_BADGE_COLOR

# Deskripsi tiap level (belum ada kolomnya di tabel `levels`, jadi disimpan
# di sini per nama level, sesuai teks di desain Figma)
DESKRIPSI_LEVEL = {
    "Mudah": "Cocok untuk memulai petualangan pertamamu. Santai dan menyenangkan!",
    "Sedang": "Butuh sedikit konsentrasi lebih untuk memilah semua bola berwarna.",
    "Sulit": "Hanya untuk para ahli! Banyak bola dan tabung yang menantang otak.",
}

WARNA_ABU_TERKUNCI = "#D9D9D9"
TEKS_ABU_TERKUNCI = "#9A9A9A"


class LevelScreen(tk.Frame):
    def __init__(self, parent, user_data, on_pilih_level=None, on_kembali=None):
        """
        :param user_data: dict {"id", "username", ...}
        :param on_pilih_level: callback(level_data: dict) -> mulai game di level itu
        :param on_kembali: callback() -> kembali ke menu utama
        """
        super().__init__(parent, bg=BG_COLOR)

        self.user_data = user_data
        self.on_pilih_level = on_pilih_level
        self.on_kembali = on_kembali

        self.level_manager = LevelManager()
        self.progres_manager = ProgressManager()

        self._muat_data()

        self._build_header()
        self._build_konten()

    # ------------------------------------------------------------
    # AMBIL DATA
    # ------------------------------------------------------------
    def _muat_data(self):
        self.semua_level = self.level_manager.get_semua_level()

        progres = self.progres_manager.get_progress_pemain(
            self.user_data["id"])
        self.current_level_pemain = progres["current_level"] if progres else "Mudah"

    # ------------------------------------------------------------
    # HEADER
    # ------------------------------------------------------------
    def _build_header(self):
        header = tk.Frame(self, bg=BG_COLOR)
        header.pack(fill="x", padx=30, pady=20)

        tk.Button(
            header, text="\u2190", font=("Arial", 14, "bold"), bg=BG_COLOR,
            fg=PRIMARY_BLUE, relief="flat", command=self._klik_kembali,
        ).pack(side="left", padx=(0, 12))

        tk.Label(
            header, text="Color Ball Sort Puzzle", font=("Arial", 16, "bold"),
            bg=BG_COLOR, fg=PRIMARY_BLUE,
        ).pack(side="left")

        tk.Label(
            header, text="\u2699", font=("Arial", 14), bg=BG_COLOR, fg="#333333",
        ).pack(side="right")

    # ------------------------------------------------------------
    # KONTEN UTAMA
    # ------------------------------------------------------------
    def _build_konten(self):
        tk.Label(
            self, text="Pilih Tingkat Kesulitan", font=("Arial", 26, "bold"),
            bg=BG_COLOR, fg=TEXT_DARK,
        ).pack(pady=(10, 4))

        tk.Label(
            self, text="Tentukan tantanganmu hari ini dan mulailah bermain!",
            font=("Arial", 11), bg=BG_COLOR, fg=TEXT_MUTED,
        ).pack(pady=(0, 30))

        area_card = tk.Frame(self, bg=BG_COLOR)
        area_card.pack()

        for level_data in self.semua_level:
            terbuka = self.level_manager.is_level_terbuka(
                level_data["id_level"], self.current_level_pemain
            )
            self._build_card_level(area_card, level_data, terbuka)

    def _build_card_level(self, parent, level_data, terbuka: bool):
        nama_level = level_data["nama_level"]
        id_level = level_data["id_level"]

        warna_tema = LEVEL_BADGE_COLOR.get(nama_level, PRIMARY_BLUE)
        warna_aktif = warna_tema if terbuka else WARNA_ABU_TERKUNCI
        warna_teks = TEXT_DARK if terbuka else TEKS_ABU_TERKUNCI

        card = tk.Frame(
            parent, bg=CARD_COLOR, highlightbackground=warna_aktif,
            highlightthickness=2, width=320, height=380,
        )
        card.pack(side="left", padx=16)
        card.pack_propagate(False)

        # --- Icon lingkaran + bintang sesuai id_level ---
        canvas_icon = tk.Canvas(card, width=80, height=80,
                                bg=CARD_COLOR, highlightthickness=0)
        canvas_icon.pack(pady=(30, 10))
        canvas_icon.create_oval(
            5, 5, 75, 75, fill=warna_aktif if terbuka else "#EDEDED", outline="")

        if terbuka:
            bintang = "\u2B50" * id_level
            canvas_icon.create_text(40, 40, text=bintang, font=("Arial", 12))
        else:
            canvas_icon.create_text(
                40, 40, text="\U0001F512", font=("Arial", 20))

        # --- Badge "TINGKAT n" ---
        tk.Label(
            card, text=f"TINGKAT {id_level}", font=("Arial", 8, "bold"),
            bg=warna_aktif if terbuka else "#EDEDED",
            fg="white" if terbuka else TEKS_ABU_TERKUNCI,
            padx=10, pady=2,
        ).pack(pady=(0, 10))

        # --- Nama level ---
        tk.Label(
            card, text=nama_level, font=("Arial", 20, "bold"),
            bg=CARD_COLOR, fg=warna_teks,
        ).pack()

        # --- Deskripsi ---
        deskripsi = DESKRIPSI_LEVEL.get(nama_level, "")
        tk.Label(
            card, text=deskripsi, font=("Arial", 9), bg=CARD_COLOR,
            fg=warna_teks, wraplength=260, justify="center",
        ).pack(pady=(8, 20), padx=16)

        # --- Tombol ---
        if terbuka:
            tk.Button(
                card, text=f"Pilih {nama_level}", font=("Arial", 11, "bold"),
                bg=warna_tema, fg="white", relief="flat", width=20, pady=8,
                command=lambda ld=level_data: self._klik_pilih_level(ld),
            ).pack(side="bottom", pady=20)
        else:
            tk.Button(
                card, text="\U0001F512 Terkunci", font=("Arial", 11, "bold"),
                bg="#EDEDED", fg=TEKS_ABU_TERKUNCI, relief="flat", width=20, pady=8,
                state="disabled",
            ).pack(side="bottom", pady=20)

    # ------------------------------------------------------------
    # AKSI
    # ------------------------------------------------------------
    def _klik_pilih_level(self, level_data):
        if self.on_pilih_level:
            self.on_pilih_level(level_data)

    def _klik_kembali(self):
        if self.on_kembali:
            self.on_kembali()
