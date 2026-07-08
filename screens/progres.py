"""
screens/progres_screen.py

Halaman "Progres" — menampilkan level terakhir, skor terbaik, ringkasan
bermain, target berikutnya, dan riwayat permainan pemain.

Dibuat sebagai class (ProgresScreen), mengikuti pola LevelSelesaiScreen,
supaya siap dipasang di main.py.

Ikon yang dipakai (dari folder aset/Icon progress/):
- Icon waktu.png            -> kotak "Total Waktu"
- Icon level selesai.png    -> kotak "Level Selesai"
- Icon riwayat permainan.png -> header card "Riwayat Permainan"

Untuk ikon lain (tombol kembali, gear, trophy peringkat, centang di
baris riwayat) belum ada asetnya, jadi masih pakai teks/emoji seperti
kode asli.

Cara pakai dari main.py nanti (kurang lebih):

    frame = ProgresScreen(
        parent,
        data_progres=data,
        on_kembali=fungsi_kembali_ke_menu,
        on_lanjut_bermain=fungsi_lanjut_bermain,
        on_lihat_semua_riwayat=fungsi_lihat_semua_riwayat,
    )
    frame.pack(fill="both", expand=True)
"""

import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from logic.progres_manager import ProgressManager
from database import queries

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDER_ICON = os.path.join(BASE_DIR, "aset", "Icon progress")

BG_COLOR = "#F6F6F6"
PRIMARY_BLUE = "#1565C0"
TEXT_MUTED = "gray"
KOTAK_BG = "#F3F5FF"
TARGET_BG = "#E9EAF4"
BORDER_COLOR = "#DDDDDD"


def _muat(nama_file, size=None):
    img = Image.open(os.path.join(FOLDER_ICON, nama_file))
    if size:
        img = img.resize(size)
    return ImageTk.PhotoImage(img)


class ProgresScreen(tk.Frame):

    def __init__(
        self,
        parent,
        user_data,
        on_kembali=None,
        on_lanjut_bermain=None,
        on_lihat_semua_riwayat=None,
    ):

        super().__init__(parent, bg=BG_COLOR)

        self.user_data = user_data

        self.progress_manager = ProgressManager()

        progress = self.progress_manager.get_progress_pemain(
            self.user_data["id"]
        )

        # Jika pemain baru
        if progress is None:
            progress = {
                "current_level": "Mudah",
                "best_score": 0
            }

        riwayat = queries.get_score_history(
            self.user_data["id"]
        )

        if riwayat is None:
            riwayat = []

        peringkat = queries.get_user_rank(
            self.user_data["id"]
        )

        if peringkat is None:
            peringkat = "-"

        jumlah_main = queries.get_total_playtime_seconds(
            self.user_data["id"]
        )

        if jumlah_main is None:
            jumlah_main = 0

        jam = jumlah_main // 3600
        menit = (jumlah_main % 3600) // 60

        current = progress["current_level"]

        if current == "Mudah":
            target = "Sedang"
            persen = 33
        elif current == "Sedang":
            target = "Sulit"
            persen = 66
        else:
            target = "Selesai"
            persen = 100

        self.data_progres = {
            "level_terakhir": current,
            "target_berikutnya": target,
            "persen_progres": persen,
            "skor_terbaik": progress["best_score"],
            "peringkat": peringkat,
            "total_waktu": f"{jam}j {menit}m",
            "level_selesai": current,
            "target_judul": f"Selesaikan level {target}",
        }

        self.riwayat = []

        for item in riwayat:

            waktu = item["waktu_bermain"]

            if hasattr(waktu, "strftime"):
                waktu = waktu.strftime("%d/%m/%Y %H:%M")

            self.riwayat.append({
                "level": item["level_reached"],
                "waktu": str(waktu),
                "skor": f'{item["score"]} Pts',
                "durasi": "-"
            })

        self.on_kembali = on_kembali
        self.on_lanjut_bermain = on_lanjut_bermain
        self.on_lihat_semua_riwayat = on_lihat_semua_riwayat

        self._muat_aset()
        self._build_konten()

    # ------------------------------------------------------------
    # ASET
    # ------------------------------------------------------------

    def _muat_aset(self):
        # Hanya 3 file ikon ini yang tersedia di folder aset/Icon progress
        self.icon_waktu = _muat("Icon waktu.png", (18, 18))
        self.icon_level_selesai = _muat("Icon level selesai.png", (18, 18))
        self.icon_riwayat = _muat("Icon riwayat permainan.png", (16, 16))

    # ------------------------------------------------------------
    # KONTEN
    # ------------------------------------------------------------
    def _build_konten(self):

        main = tk.Frame(self, bg=BG_COLOR)
        main.pack(fill="both", expand=True, padx=30, pady=20)

        self._build_header(main)
        self._build_card_atas(main)
        self._build_bagian_tengah(main)
        self._build_riwayat(main)

    # ---------------- HEADER ----------------

    def _build_header(self, main):

        header = tk.Frame(main, bg=BG_COLOR)
        header.pack(fill="x")

        tk.Button(
            header,
            text="← Progres",
            relief="flat",
            bg=BG_COLOR,
            fg=PRIMARY_BLUE,
            font=("Poppins", 11, "bold"),
            cursor="hand2",
            command=self._klik_kembali,
        ).pack(side="left")

    # ---------------- CARD ATAS (LEVEL + SKOR) ----------------

    def _build_card_atas(self, main):

        atas = tk.Frame(main, bg=BG_COLOR)
        atas.pack(pady=20)

        # ------------ LEVEL ------------
        level = tk.Frame(
            atas,
            bg="white",
            highlightbackground=PRIMARY_BLUE,
            highlightthickness=1,
            width=330,
            height=120,
        )
        level.pack(side="left")
        level.pack_propagate(False)

        tk.Label(
            level, text="LEVEL TERAKHIR", bg="white", fg="gray",
            font=("Poppins", 8),
        ).pack(anchor="w", padx=12, pady=(10, 0))

        tk.Label(
            level, text=self.data_progres["level_terakhir"], bg="white",
            fg=PRIMARY_BLUE, font=("Poppins", 20, "bold"),
        ).pack(anchor="w", padx=12)

        baris_progres = tk.Frame(level, bg="white")
        baris_progres.pack(fill="x", padx=12, pady=(5, 0))

        tk.Label(
            baris_progres,
            text=f"Menuju {self.data_progres['target_berikutnya']}",
            bg="white", fg="gray", font=("Poppins", 8),
        ).pack(side="left")

        tk.Label(
            baris_progres,
            text=f"{self.data_progres['persen_progres']}%",
            bg="white", fg=PRIMARY_BLUE, font=("Poppins", 8, "bold"),
        ).pack(side="right")

        progress = ttk.Progressbar(
            level, length=290, value=self.data_progres["persen_progres"]
        )
        progress.pack(anchor="w", padx=12, pady=5)

        # ------------ SKOR ------------
        skor = tk.Frame(atas, bg=PRIMARY_BLUE, width=460, height=120)
        skor.pack(side="left", padx=15)
        skor.pack_propagate(False)

        tk.Label(
            skor, text="SKOR TERBAIK", bg=PRIMARY_BLUE, fg="white",
            font=("Poppins", 8),
        ).pack(anchor="w", padx=15, pady=(10, 0))

        tk.Label(
            skor, text=self.data_progres["skor_terbaik"], bg=PRIMARY_BLUE,
            fg="white", font=("Poppins", 24, "bold"),
        ).pack(anchor="w", padx=15)

        baris_rank = tk.Frame(skor, bg=PRIMARY_BLUE)
        baris_rank.pack(anchor="w", padx=15, pady=8)

        tk.Label(
            baris_rank, text="🏆", bg=PRIMARY_BLUE,
        ).pack(side="left", padx=(0, 6))

        tk.Label(
            baris_rank,
            text=f"Peringkat #{self.data_progres['peringkat']} di Leaderboard",
            bg=PRIMARY_BLUE, fg="white", font=("Poppins", 9),
        ).pack(side="left")

    # ---------------- BAGIAN TENGAH (RINGKASAN + TARGET) ----------------

    def _build_bagian_tengah(self, main):

        tengah = tk.Frame(main, bg=BG_COLOR)
        tengah.pack(pady=10)

        # ------------ RINGKASAN ------------
        ringkasan = tk.Frame(
            tengah, bg="white", width=280, height=180,
            highlightbackground=BORDER_COLOR, highlightthickness=1,
        )
        ringkasan.pack(side="left")
        ringkasan.pack_propagate(False)

        tk.Label(
            ringkasan, text="Ringkasan Bermain", bg="white",
            font=("Poppins", 11, "bold"),
        ).pack(anchor="w", padx=12, pady=10)

        kotak1 = tk.Frame(ringkasan, bg=KOTAK_BG)
        kotak1.pack(fill="x", padx=12, pady=5)

        tk.Label(
            kotak1, image=self.icon_waktu, bg=PRIMARY_BLUE, width=30,
        ).pack(side="left", padx=6, pady=8)

        tk.Label(
            kotak1,
            text=f"Total Waktu\n{self.data_progres['total_waktu']}",
            justify="left", bg=KOTAK_BG, font=("Poppins", 9),
        ).pack(anchor="w", padx=10)

        kotak2 = tk.Frame(ringkasan, bg=KOTAK_BG)
        kotak2.pack(fill="x", padx=12, pady=5)

        tk.Label(
            kotak2, image=self.icon_level_selesai, bg=PRIMARY_BLUE, width=30,
        ).pack(side="left", padx=6, pady=8)

        tk.Label(
            kotak2,
            text=f"Level Selesai\n{self.data_progres['level_selesai']}",
            justify="left", bg=KOTAK_BG, font=("Poppins", 9),
        ).pack(anchor="w", padx=10)

        # ------------ TARGET ------------
        target = tk.Frame(tengah, bg=TARGET_BG, width=280, height=180)
        target.pack(side="left")
        target.pack_propagate(False)

        tk.Label(
            target, text="Target Berikutnya", bg=TARGET_BG,
            font=("Poppins", 11, "bold"),
        ).pack(pady=(35, 10))

        tk.Label(
            target, text=self.data_progres["target_judul"], bg=TARGET_BG,
            fg="gray", font=("Poppins", 9),
        ).pack()

        tk.Button(
            target, text="Lanjut Bermain", bg=PRIMARY_BLUE, fg="white",
            relief="flat", width=18, cursor="hand2",
            command=self._klik_lanjut_bermain,
        ).pack(pady=25)

    # ---------------- RIWAYAT ----------------

    def _build_riwayat(self, main):

        bawah = tk.Frame(
            main, bg="white",
            highlightbackground=BORDER_COLOR, highlightthickness=1,
        )
        bawah.pack(fill="x", pady=20)

        header2 = tk.Frame(bawah, bg="#F4F6FF")
        header2.pack(fill="x")

        tk.Label(
            header2, image=self.icon_riwayat, bg="#F4F6FF",
        ).pack(side="left", padx=(10, 4), pady=8)

        tk.Label(
            header2, text="Riwayat Permainan", bg="#F4F6FF",
            font=("Poppins", 10, "bold"),
        ).pack(side="left", pady=8)

        tk.Label(
            header2, text="Lihat Semua", bg="#F4F6FF", fg=PRIMARY_BLUE,
            font=("Poppins", 8), cursor="hand2",
        ).pack(side="right", padx=10)

        for item in self.riwayat:

            baris = tk.Frame(bawah, bg="white")
            baris.pack(fill="x", padx=10, pady=8)

            tk.Label(
                baris, text="✓", bg="#DFF7E2", fg="#1E8E3E",
                font=("Poppins", 10, "bold"), width=2,
            ).pack(side="left")

            info = tk.Frame(baris, bg="white")
            info.pack(side="left", padx=10)

            tk.Label(
                info, text=item["level"], bg="white",
                font=("Poppins", 9, "bold"),
            ).pack(anchor="w")

            tk.Label(
                info, text=item["waktu"], bg="white", fg="gray",
                font=("Poppins", 8),
            ).pack(anchor="w")

            tk.Label(
                baris, text=item["skor"], bg="white",
                font=("Poppins", 9, "bold"),
            ).pack(side="right", padx=20)

            tk.Label(
                baris, text=item["durasi"], bg="white", fg="gray",
                font=("Poppins", 8),
            ).pack(side="right")

    # ------------------------------------------------------------
    # AKSI (tinggal manggil callback yang dikasih dari luar)
    # ------------------------------------------------------------
    def _klik_kembali(self):
        if self.on_kembali:
            self.on_kembali()

    def _klik_lanjut_bermain(self):
        if self.on_lanjut_bermain:
            self.on_lanjut_bermain()


# ------------------------------------------------------------
# MODE TES MANDIRI
# ------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Progres")
    root.geometry("800x650")
    root.state("zoomed")
    root.configure(bg=BG_COLOR)

    dummy_user = {
        "id": 1,
        "username": "Admin"
    }

    ProgresScreen(
        root,
        user_data=dummy_user
    ).pack(fill="both", expand=True)

    root.mainloop()
