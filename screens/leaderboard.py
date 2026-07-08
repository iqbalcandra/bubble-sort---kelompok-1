"""
screens/leaderboard_screen.py

Halaman "Papan Peringkat" — menampilkan Top 5 pemain terbaik.

Dibuat sebagai class (LeaderboardScreen), mengikuti pola LoginScreen
(window mandiri dengan self.root, bukan Frame yang ditempel ke parent),
karena halaman ini dipanggil sebagai proses terpisah lewat subprocess,
sama seperti login_screen.py -> menu_screen.py.

Ikon yang dipakai (dari folder aset/Icon papan peringkat/):
- Icon trophy.png     -> header biru "Top 5 Pemain Terbaik"
- Icon kembali.png    -> tombol Kembali
- Icon ulang.png      -> tombol Muat Ulang
- Icon diperbarui.png -> info kecil di footer
- Button setting.png  -> gear kanan atas
- Peringkat 1.png ... Peringkat 4.png -> badge bulat untuk 4 rank teratas
  (rank 5 / peringkat pemain sendiri digambar pakai Canvas, karena tidak
  ada file "Peringkat 5.png")

FIX (2026-07-08):
- Frame kolom_rank, kolom_nama, kolom_level dulunya hanya diberi `width`
  tanpa `height`, padahal pack_propagate(False) dipanggil di atasnya.
  Akibatnya tinggi Frame collapse ke ~0/1px sehingga badge peringkat,
  teks nama, dan pill level ter-clip / tidak kelihatan sama sekali
  (padahal widget & gambar sebenarnya berhasil dibuat).
  Fix: tambahkan `height=ROW_HEIGHT` pada ketiga Frame tersebut.
"""

import os
import sys
import subprocess
import tkinter as tk

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDER_ICON = os.path.join(BASE_DIR, "aset", "Icon papan peringkat")

BG_COLOR = "#F5F6FA"
PRIMARY_BLUE = "#0056C6"
TEXT_MUTED = "gray40"
BORDER_COLOR = "#E5E5E5"
HIGHLIGHT_BG = "#EAF1FC"

# Tinggi tetap untuk kolom yang pakai pack_propagate(False),
# supaya isinya (badge/teks/pill) tidak ke-clip.
ROW_HEIGHT = 40

# Lebar kolom dalam PIXEL (bukan karakter huruf!) — dipakai sama persis
# di header kolom (_build_kolom_judul) maupun di baris data
# (_build_baris_data) supaya semua kolom benar-benar lurus/align.
COL_W_RANK = 90
COL_W_NAMA = 210
COL_W_SKOR = 100
COL_W_LEVEL = 110
COL_W_TANGGAL = 130


def _muat(nama_file, size=None):
    from PIL import Image, ImageTk
    img = Image.open(os.path.join(FOLDER_ICON, nama_file))
    if size:
        img = img.resize(size)
    return ImageTk.PhotoImage(img)


class LeaderboardScreen:

    def __init__(self, data=None):

        # ===============================
        # WINDOW
        # ===============================

        self.root = tk.Tk()
        self.root.title("Leaderboard")
        self.root.geometry("900x650")
        self.root.state("zoomed")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        # Data default (dummy) kalau belum dikasih dari luar
        self.data = data or [
            {
                "peringkat": 1, "nama": "Andi Pratama", "skor": "2.450",
                "level": "Hard", "tanggal": "13 July 2026",
                "is_top": True, "is_current_user": False,
            },
            {
                "peringkat": 2, "nama": "Siti Rahayu", "skor": "2.180",
                "level": "Hard", "tanggal": "13 July 2026",
                "is_top": False, "is_current_user": False,
            },
            {
                "peringkat": 3, "nama": "Budi Santoso", "skor": "1.950",
                "level": "Medium", "tanggal": "13 July 2026",
                "is_top": False, "is_current_user": False,
            },
            {
                "peringkat": 4, "nama": "Lani Wijaya", "skor": "1.720",
                "level": "Easy", "tanggal": "13 July 2026",
                "is_top": False, "is_current_user": False,
            },
            {
                "peringkat": 5, "nama": "Marchel", "skor": "1.580",
                "level": "Medium", "tanggal": "Hari Ini",
                "is_top": False, "is_current_user": True,
            },
        ]

        self._muat_aset()
        self._build_ui()

    # ------------------------------------------------------------
    # ASET
    # ------------------------------------------------------------
    def _muat_aset(self):
        self.icon_trophy = _muat("Icon trophy.png", (18, 18))
        self.icon_kembali = _muat("Icon kembali.png", (16, 16))
        self.icon_ulang = _muat("Icon ulang.png", (16, 16))
        self.icon_diperbarui = _muat("Icon diperbarui.png", (14, 14))
        self.icon_setting = _muat("Button setting.png", (22, 22))

        self.icon_peringkat = {
            1: _muat("Peringkat 1.png", (28, 28)),
            2: _muat("Peringkat 2.png", (28, 28)),
            3: _muat("Peringkat 3.png", (28, 28)),
            4: _muat("Peringkat 4.png", (28, 28)),
        }

    # ------------------------------------------------------------
    # UI
    # ------------------------------------------------------------
    def _build_ui(self):

        main = tk.Frame(self.root, bg=BG_COLOR)
        main.pack(fill="both", expand=True, padx=60, pady=30)

        self._build_header(main)

        card = tk.Frame(
            main, bg="white",
            highlightbackground=BORDER_COLOR, highlightthickness=1,
        )
        card.pack(fill="both", expand=True, pady=(15, 0))

        self._build_card_header(card)
        self._build_kolom_judul(card)
        self._build_baris_data(card)
        self._build_footer(card)

    # ---------------- HEADER LUAR ----------------

    def _build_header(self, main):

        header = tk.Frame(main, bg=BG_COLOR)
        header.pack(fill="x")

        tk.Label(
            header, text="Papan Peringkat", font=("Arial", 20, "bold"),
            bg=BG_COLOR, fg=PRIMARY_BLUE,
        ).pack(side="left")

        tk.Label(
            header, image=self.icon_setting, bg=BG_COLOR,
        ).pack(side="right")

    # ---------------- HEADER CARD (BIRU) ----------------

    def _build_card_header(self, card):

        card_header = tk.Frame(card, bg=PRIMARY_BLUE, height=45)
        card_header.pack(fill="x")

        tk.Label(
            card_header, image=self.icon_trophy, bg=PRIMARY_BLUE,
        ).pack(side="left", padx=(20, 8), pady=10)

        tk.Label(
            card_header, text="Top 5 Pemain Terbaik", bg=PRIMARY_BLUE,
            fg="white", font=("Arial", 12, "bold"),
        ).pack(side="left", pady=10)

    # ---------------- JUDUL KOLOM ----------------

    def _build_kolom_judul(self, card):

        judul = tk.Frame(card, bg="white")
        judul.pack(fill="x", padx=30, pady=(15, 5))

        # Lebar tiap kolom judul HARUS sama persis dengan lebar kolom
        # di baris data (_build_baris_data), supaya lurus/align.
        judul_data = [
            ("PERINGKAT", COL_W_RANK),
            ("NAMA", COL_W_NAMA),
            ("SKOR", COL_W_SKOR),
            ("LEVEL", COL_W_LEVEL),
            ("TANGGAL", COL_W_TANGGAL),
        ]

        for text, width in judul_data:
            kolom = tk.Frame(judul, bg="white", width=width, height=20)
            kolom.pack(side="left")
            kolom.pack_propagate(False)

            tk.Label(
                kolom, text=text, bg="white", fg="gray50",
                font=("Arial", 8, "bold"), anchor="w",
            ).pack(side="left", fill="x")

    # ---------------- BARIS DATA ----------------

    def _build_baris_data(self, card):

        for pemain in self.data:

            bg_row = HIGHLIGHT_BG if pemain["is_current_user"] else "white"

            row = tk.Frame(card, bg=bg_row)
            row.pack(fill="x", padx=30, pady=4)

            # ------ Kolom Peringkat (badge bulat) ------
            kolom_rank = tk.Frame(
                row, bg=bg_row, width=COL_W_RANK, height=ROW_HEIGHT)
            kolom_rank.pack(side="left")
            kolom_rank.pack_propagate(False)

            rank = pemain["peringkat"]

            if rank in self.icon_peringkat:
                tk.Label(
                    kolom_rank, image=self.icon_peringkat[rank], bg=bg_row,
                ).pack(side="left", pady=8)
            else:
                # Rank 5 / peringkat pemain sendiri, tidak ada asetnya
                canvas = tk.Canvas(
                    kolom_rank, width=28, height=28, bg=bg_row,
                    highlightthickness=0,
                )
                canvas.pack(side="left", pady=8)
                canvas.create_oval(1, 1, 27, 27, fill=PRIMARY_BLUE, outline="")
                canvas.create_text(
                    14, 14, text=str(rank), fill="white",
                    font=("Arial", 10, "bold"),
                )

            # ------ Kolom Nama ------
            kolom_nama = tk.Frame(
                row, bg=bg_row, width=COL_W_NAMA, height=ROW_HEIGHT)
            kolom_nama.pack(side="left")
            kolom_nama.pack_propagate(False)

            warna_nama = PRIMARY_BLUE if (
                pemain["is_top"] or pemain["is_current_user"]
            ) else "black"

            tk.Label(
                kolom_nama, text=pemain["nama"], bg=bg_row, fg=warna_nama,
                font=("Arial", 10, "bold"), anchor="w",
            ).pack(anchor="w", pady=(8, 0))

            if pemain["is_current_user"]:
                tk.Label(
                    kolom_nama, text="PERINGKAT ANDA", bg=bg_row,
                    fg=PRIMARY_BLUE, font=("Arial", 7, "bold"), anchor="w",
                ).pack(anchor="w")

            # ------ Kolom Skor ------
            kolom_skor = tk.Frame(
                row, bg=bg_row, width=COL_W_SKOR, height=ROW_HEIGHT)
            kolom_skor.pack(side="left")
            kolom_skor.pack_propagate(False)

            warna_skor = "#D97706" if pemain["is_top"] else "black"

            tk.Label(
                kolom_skor, text=pemain["skor"], bg=bg_row,
                fg=warna_skor, font=("Arial", 11, "bold"), anchor="w",
            ).pack(side="left", pady=8)

            # ------ Kolom Level (pill) ------
            kolom_level = tk.Frame(
                row, bg=bg_row, width=COL_W_LEVEL, height=ROW_HEIGHT)
            kolom_level.pack(side="left")
            kolom_level.pack_propagate(False)

            if pemain["is_current_user"]:
                pill_bg, pill_fg = PRIMARY_BLUE, "white"
            else:
                pill_bg, pill_fg = "#E5E5E5", "black"

            tk.Label(
                kolom_level, text=pemain["level"], bg=pill_bg, fg=pill_fg,
                font=("Arial", 8, "bold"), padx=10, pady=2,
            ).pack(anchor="w", pady=8)

            # ------ Kolom Tanggal ------
            kolom_tanggal = tk.Frame(
                row, bg=bg_row, width=COL_W_TANGGAL, height=ROW_HEIGHT)
            kolom_tanggal.pack(side="left")
            kolom_tanggal.pack_propagate(False)

            warna_tanggal = PRIMARY_BLUE if pemain["is_current_user"] else "gray40"

            tk.Label(
                kolom_tanggal, text=pemain["tanggal"], bg=bg_row,
                fg=warna_tanggal, font=("Arial", 9), anchor="w",
            ).pack(side="left", pady=8)

    # ---------------- FOOTER ----------------

    def _build_footer(self, card):

        footer = tk.Frame(card, bg="white")
        footer.pack(fill="x", side="bottom", padx=30, pady=15)

        info = tk.Frame(footer, bg="white")
        info.pack(side="left")

        tk.Label(
            info, image=self.icon_diperbarui, bg="white",
        ).pack(side="left", padx=(0, 6))

        tk.Label(
            info, text="Papan peringkat diperbarui setiap 10 menit.",
            bg="white", fg=TEXT_MUTED, font=("Arial", 9),
        ).pack(side="left")

        tk.Button(
            footer, text=" Muat Ulang", image=self.icon_ulang,
            compound="left", bg=PRIMARY_BLUE, fg="white", relief="flat",
            font=("Arial", 9, "bold"), padx=12, pady=6, cursor="hand2",
            command=self.muat_ulang,
        ).pack(side="right")

        tk.Button(
            footer, text=" Kembali", image=self.icon_kembali,
            compound="left", bg="white", fg=PRIMARY_BLUE, relief="solid",
            bd=1, font=("Arial", 9, "bold"), padx=12, pady=6, cursor="hand2",
            command=self.kembali,
        ).pack(side="right", padx=8)

    # ------------------------------------------------------------
    # AKSI
    # ------------------------------------------------------------
    def kembali(self):

        self.root.destroy()

        menu_path = os.path.join(BASE_DIR, "screens", "menu_screen.py")
        subprocess.Popen([sys.executable, menu_path])

    def muat_ulang(self):
        # TODO: nanti diganti query ulang ke database (tabel scores/progress)
        print("Muat ulang leaderboard (belum konek database)")

    # ------------------------------------------------------------
    # RUN
    # ------------------------------------------------------------
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = LeaderboardScreen()
    app.run()
