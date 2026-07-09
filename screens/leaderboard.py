"""
screens/leaderboard_screen.py

Halaman "Papan Peringkat" (Leaderboard) - menampilkan Top 5 skor
tertinggi Baris milik pemain yang sedang login
di-highlight, sesuai desain.
"""

import tkinter as tk

from database import queries
from theme import BG_COLOR, CARD_COLOR, PRIMARY_BLUE, TEXT_DARK, TEXT_MUTED

WARNA_PERINGKAT = {
    1: "#F5C518",  # emas
    2: "#9CA3AF",  # perak
    3: "#B45309",  # perunggu
    4: "#E05252"   # merah
}
WARNA_PERINGKAT_DEFAULT = "#D9D9D9"
HIGHLIGHT_BG = "#EAF0FD"

# Lebar kolom tabel dalam PIKSEL (bukan karakter). Dipakai SAMA PERSIS di
# header dan tiap baris data supaya kolom benar-benar lurus -- sebelumnya
# header pakai width=N karakter dengan font 9pt bold, sedangkan tiap baris
# data pakai width=N karakter yang beda dengan font yang beda juga (11pt
# bold untuk skor, dst). Lebar 1 karakter di font berbeda = jumlah piksel
# yang beda, jadi kolom gak akan pernah lurus walau angkanya kelihatan
# masuk akal. Piksel tetap = presisi, gak peduli font apa pun dipakai.
LEBAR_KOLOM_PERINGKAT = 90
LEBAR_KOLOM_NAMA = 340
LEBAR_KOLOM_SKOR = 200
LEBAR_KOLOM_LEVEL = 180
LEBAR_KOLOM_TANGGAL = 200


class LeaderboardScreen(tk.Frame):
    def __init__(self, parent, user_data, on_kembali=None):
        """
        :param user_data: dict {"id", "username", ...} pemain yang sedang login
        :param on_kembali: callback() -> kembali ke menu utama
        """
        super().__init__(parent, bg=BG_COLOR)

        self.user_data = user_data
        self.on_kembali = on_kembali

        self._muat_data()

        self._build_header()
        self._build_card_leaderboard()

    # ------------------------------------------------------------
    # AMBIL DATA DARI DATABASE
    # ------------------------------------------------------------
    def _muat_data(self):
        self.daftar_skor = queries.get_top_scores(limit=5)
        self.rank_sekarang = queries.get_user_rank(self.user_data["id"])

    # ------------------------------------------------------------
    # HEADER
    # ------------------------------------------------------------
    def _build_header(self):
        header = tk.Frame(self, bg=BG_COLOR)
        header.pack(fill="x", padx=30, pady=20)

        tk.Label(
            header, text="Papan Peringkat", font=("Arial", 20, "bold"),
            bg=BG_COLOR, fg=PRIMARY_BLUE,
        ).pack(side="left")

    # ------------------------------------------------------------
    # CARD UTAMA (banner biru + tabel + footer)
    # ------------------------------------------------------------

    def _build_card_leaderboard(self):
        card = tk.Frame(self, bg=CARD_COLOR,
                        highlightbackground="#E0E0E0", highlightthickness=1)
        card.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        # --- Banner biru atas ---
        banner = tk.Frame(card, bg=PRIMARY_BLUE, height=60)
        banner.pack(fill="x")
        banner.pack_propagate(False)

        tk.Label(
            banner, text="\U0001F3C6  Top 5 Pemain Terbaik", font=("Arial", 13, "bold"),
            bg=PRIMARY_BLUE, fg="white",
        ).pack(side="left", padx=24, pady=14)

        # --- Header kolom tabel ---
        header_kolom = tk.Frame(card, bg=CARD_COLOR)
        header_kolom.pack(fill="x", padx=24, pady=(16, 6))

        self._label_kolom(header_kolom, "PERINGKAT", LEBAR_KOLOM_PERINGKAT)
        self._label_kolom(header_kolom, "NAMA", LEBAR_KOLOM_NAMA)
        self._label_kolom(header_kolom, "SKOR", LEBAR_KOLOM_SKOR)
        self._label_kolom(header_kolom, "LEVEL", LEBAR_KOLOM_LEVEL)
        self._label_kolom(header_kolom, "TANGGAL", LEBAR_KOLOM_TANGGAL)

        garis = tk.Frame(card, bg="#E0E0E0", height=1)
        garis.pack(fill="x", padx=24)

        # --- Baris data ---
        if not self.daftar_skor:
            tk.Label(
                card, text="Belum ada data skor. Jadilah yang pertama bermain!",
                font=("Arial", 10), bg=CARD_COLOR, fg=TEXT_MUTED,
            ).pack(pady=30)
        else:
            for index, entri in enumerate(self.daftar_skor):
                self._build_baris(card, index + 1, entri)

        # --- Footer ---
        footer = tk.Frame(card, bg=BG_COLOR)
        footer.pack(fill="x", side="bottom", padx=24, pady=16)

        tk.Label(
            footer, text="\u2139  Papan peringkat diperbarui secara real-time saat halaman dibuka.",
            font=("Arial", 9), bg=BG_COLOR, fg=TEXT_MUTED,
        ).pack(side="left")

        tk.Button(
            footer, text="\u2190 Kembali", font=("Arial", 10, "bold"),
            bg=CARD_COLOR, fg=PRIMARY_BLUE, relief="solid", bd=1, padx=14, pady=6,
            command=self._klik_kembali,
        ).pack(side="right", padx=6)

        tk.Button(
            footer, text="\u21BB Muat Ulang", font=("Arial", 10, "bold"),
            bg=PRIMARY_BLUE, fg="white", relief="flat", padx=14, pady=6,
            command=self._klik_muat_ulang,
        ).pack(side="right", padx=6)

    def _label_kolom(self, parent, teks, lebar_piksel):
        # Bungkus Label dengan Frame ber-lebar PIKSEL TETAP (pack_propagate
        # False supaya Frame tidak ikut menyusut/melebar ke ukuran teks).
        # Ini memastikan kolom header punya lebar piksel yang SAMA PERSIS
        # dengan kolom data di _build_baris(), apa pun font yang dipakai.
        wrapper = tk.Frame(parent, bg=CARD_COLOR,
                           width=lebar_piksel, height=22)
        wrapper.pack(side="left")
        wrapper.pack_propagate(False)

        tk.Label(
            wrapper, text=teks, font=("Arial", 9, "bold"), bg=CARD_COLOR,
            fg=TEXT_MUTED, anchor="w",
        ).pack(fill="both", expand=True)

    # ------------------------------------------------------------
    # SATU BARIS DATA PEMAIN
    # ------------------------------------------------------------
    def _build_baris(self, parent, peringkat, entri):
        adalah_user_sekarang = entri["username"] == self.user_data["username"]
        bg_baris = HIGHLIGHT_BG if adalah_user_sekarang else CARD_COLOR

        baris = tk.Frame(parent, bg=bg_baris)
        baris.pack(fill="x", padx=24, pady=1, ipady=8)

        # --- Kolom PERINGKAT (badge bulat + nomor) ---
        kolom_peringkat = tk.Frame(
            baris, bg=bg_baris, width=LEBAR_KOLOM_PERINGKAT, height=28)
        kolom_peringkat.pack(side="left")
        kolom_peringkat.pack_propagate(False)

        warna_badge = WARNA_PERINGKAT.get(peringkat, WARNA_PERINGKAT_DEFAULT)
        badge = tk.Canvas(kolom_peringkat, width=28, height=28,
                          bg=bg_baris, highlightthickness=0)
        badge.create_oval(2, 2, 26, 26, fill=warna_badge, outline="")
        badge.create_text(14, 14, text=str(peringkat),
                          fill="white", font=("Arial", 9, "bold"))
        badge.pack(side="left")

        # --- Kolom NAMA ---
        kolom_nama = tk.Frame(baris, bg=bg_baris,
                              width=LEBAR_KOLOM_NAMA, height=28)
        kolom_nama.pack(side="left")
        kolom_nama.pack_propagate(False)

        nama_teks = entri["username"]
        if adalah_user_sekarang:
            nama_teks += "  (Anda)"

        tk.Label(
            kolom_nama, text=nama_teks, font=(
                "Arial", 10, "bold" if adalah_user_sekarang else "normal"),
            bg=bg_baris, fg=PRIMARY_BLUE if adalah_user_sekarang else TEXT_DARK,
            anchor="w",
        ).pack(fill="both", expand=True)

        # --- Kolom SKOR ---
        kolom_skor = tk.Frame(baris, bg=bg_baris,
                              width=LEBAR_KOLOM_SKOR, height=28)
        kolom_skor.pack(side="left")
        kolom_skor.pack_propagate(False)

        tk.Label(
            kolom_skor, text=f"{entri['score']:,}".replace(",", "."), font=("Arial", 11, "bold"),
            bg=bg_baris, fg=TEXT_DARK, anchor="w",
        ).pack(fill="both", expand=True)

        # --- Kolom LEVEL ---
        kolom_level = tk.Frame(
            baris, bg=bg_baris, width=LEBAR_KOLOM_LEVEL, height=28)
        kolom_level.pack(side="left")
        kolom_level.pack_propagate(False)

        tk.Label(
            kolom_level, text=entri["level_reached"], font=("Arial", 9), bg=bg_baris,
            fg=TEXT_MUTED, anchor="w",
        ).pack(fill="both", expand=True)

        # --- Kolom TANGGAL ---
        kolom_tanggal = tk.Frame(
            baris, bg=bg_baris, width=LEBAR_KOLOM_TANGGAL, height=28)
        kolom_tanggal.pack(side="left")
        kolom_tanggal.pack_propagate(False)

        tk.Label(
            kolom_tanggal, text=str(entri["waktu_bermain"]), font=("Arial", 9), bg=bg_baris,
            fg=TEXT_MUTED, anchor="w",
        ).pack(fill="both", expand=True)

    # ------------------------------------------------------------
    # AKSI TOMBOL
    # ------------------------------------------------------------
    def _klik_kembali(self):
        if self.on_kembali:
            self.on_kembali()

    def _klik_muat_ulang(self):
        """Ambil ulang data terbaru dari database, lalu render ulang seluruh UI."""
        for widget in self.winfo_children():
            widget.destroy()

        self._muat_data()
        self._build_header()
        self._build_card_leaderboard()
