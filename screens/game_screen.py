
import tkinter as tk
from tkinter import font as tkfont
import random
import copy

from logic.timer_manager import TimerManager
from logic.score_manager import ScoreManager
from logic.undo_manager import UndoManager


# ---------------------------------------------------------------------------
# Palet warna & konfigurasi visual (disesuaikan dengan desain Figma)
# ---------------------------------------------------------------------------
BG_COLOR = "#F1F2FB"          # background lavender muda
CARD_COLOR = "#FFFFFF"
PRIMARY_BLUE = "#1D4ED8"
PRIMARY_BLUE_DARK = "#1E3A8A"
TEXT_DARK = "#1F2330"
TEXT_MUTED = "#6B7280"

# Warna badge per tingkat level
LEVEL_BADGE_COLOR = {
    "Mudah": "#1D4ED8",
    "Sedang": "#B45309",
    "Sulit": "#B91C1C",
}

# Palet warna bola, dipakai berurutan sesuai jumlah_warna level
WARNA_BOLA = [
    "#EF4444",  # merah
    "#3B82F6",  # biru
    "#F5C518",  # kuning
    "#10B981",  # hijau
    "#8B5CF6",  # ungu
    "#F97316",  # oranye
    "#EC4899",  # pink
]

KAPASITAS_TABUNG = 4
LEBAR_TABUNG = 74
TINGGI_TABUNG = 260
JARAK_TABUNG = 24
RADIUS_BOLA = 26


def generate_board(jumlah_warna: int, jumlah_tabung: int) -> list:
    """
    Membuat susunan awal papan permainan secara acak.
    jumlah_tabung = jumlah_warna (terisi) + 2 tabung kosong (sesuai laporan 2.1).
    """
    bola_semua = []
    for i in range(jumlah_warna):
        bola_semua += [i] * KAPASITAS_TABUNG
    random.shuffle(bola_semua)

    papan = [[] for _ in range(jumlah_tabung)]
    idx = 0
    for t in range(jumlah_warna):
        for _ in range(KAPASITAS_TABUNG):
            papan[t].append(bola_semua[idx])
            idx += 1
    # sisa tabung (2 terakhir) dibiarkan kosong sebagai ruang gerak
    return papan


class GameScreen(tk.Frame):
    def __init__(self, master, controller, level_data: dict, user_id: int):
        """
        :param master: parent Tkinter widget
        :param controller: objek aplikasi utama, harus punya method show_frame(nama, **kwargs)
                            untuk navigasi antar screen (level_screen, result_screen, menu_screen)
        :param level_data: dict berisi konfigurasi level, mis:
            {
                "id_level": 1, "nama_level": "Mudah",
                "jumlah_warna": 3, "jumlah_tabung": 5,
                "timer": 120, "skor_dasar": 100
            }
        :param user_id: id pemain yang sedang login
        """
        super().__init__(master, bg=BG_COLOR)
        self.controller = controller
        self.level_data = level_data
        self.user_id = user_id

        self.font_judul = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        self.font_badge = tkfont.Font(family="Segoe UI", size=9, weight="bold")
        self.font_label = tkfont.Font(family="Segoe UI", size=9, weight="bold")
        self.font_angka = tkfont.Font(family="Segoe UI", size=14, weight="bold")
        self.font_tombol = tkfont.Font(family="Segoe UI", size=10, weight="bold")

        # --- state permainan ---
        self.papan = generate_board(level_data["jumlah_warna"], level_data["jumlah_tabung"])
        self.tabung_terpilih = None  # index tabung yang sedang dipilih (None jika belum ada)
        self.selesai = False

        # --- manager logic ---
        self.score_manager = ScoreManager()
        self.undo_manager = UndoManager(batas_riwayat=1)
        self.timer_manager = TimerManager(
            widget=self,
            durasi_detik=level_data["timer"],
            on_tick=self._update_label_waktu,
            on_timeout=self._saat_waktu_habis,
        )

        self._bangun_ui()
        self._gambar_papan()
        self.timer_manager.mulai()

    # ------------------------------------------------------------------
    # UI Layout
    # ------------------------------------------------------------------
    def _bangun_ui(self):
        # ---------- HEADER ----------
        header = tk.Frame(self, bg=CARD_COLOR, height=70)
        header.pack(side="top", fill="x")
        header.pack_propagate(False)

        btn_home = tk.Button(
            header, text="\u2302", font=("Segoe UI", 14), bg="#EEF0FB", fg=PRIMARY_BLUE,
            relief="flat", bd=0, width=3, cursor="hand2",
            command=self._ke_menu_utama,
        )
        btn_home.pack(side="left", padx=(16, 8), pady=14)

        judul_frame = tk.Frame(header, bg=CARD_COLOR)
        judul_frame.pack(side="left", pady=8)
        tk.Label(judul_frame, text="Color Sort Ball", font=self.font_judul,
                 bg=CARD_COLOR, fg=PRIMARY_BLUE).pack(anchor="w")

        badge_color = LEVEL_BADGE_COLOR.get(self.level_data["nama_level"], PRIMARY_BLUE)
        badge = tk.Label(
            judul_frame,
            text=f'{self.level_data["nama_level"]} - Level {self.level_data.get("id_level", 1)}',
            font=self.font_badge, bg=badge_color, fg="white", padx=8, pady=1,
        )
        badge.pack(anchor="w", pady=(2, 0))

        # WAKTU & SKOR di tengah header
        info_frame = tk.Frame(header, bg=CARD_COLOR)
        info_frame.place(relx=0.5, rely=0.5, anchor="center")

        waktu_box = tk.Frame(info_frame, bg=CARD_COLOR)
        waktu_box.pack(side="left", padx=20)
        tk.Label(waktu_box, text="WAKTU", font=self.font_label,
                 bg=CARD_COLOR, fg=TEXT_MUTED).pack()
        self.label_waktu = tk.Label(
            waktu_box, text=self.timer_manager.get_format_waktu(),
            font=self.font_angka, bg=CARD_COLOR, fg=PRIMARY_BLUE,
        )
        self.label_waktu.pack()

        skor_box = tk.Frame(info_frame, bg=CARD_COLOR)
        skor_box.pack(side="left", padx=20)
        tk.Label(skor_box, text="SKOR", font=self.font_label,
                 bg=CARD_COLOR, fg=TEXT_MUTED).pack()
        self.label_skor = tk.Label(
            skor_box, text="0", font=self.font_angka, bg=CARD_COLOR, fg=PRIMARY_BLUE,
        )
        self.label_skor.pack()

        btn_gear = tk.Label(header, text="\u2699", font=("Segoe UI", 14),
                             bg="#EEF0FB", fg=PRIMARY_BLUE, padx=10, pady=6)
        btn_gear.pack(side="right", padx=16)

        # ---------- AREA PERMAINAN (CANVAS) ----------
        area = tk.Frame(self, bg=BG_COLOR)
        area.pack(side="top", fill="both", expand=True)

        lebar_canvas = self.level_data["jumlah_tabung"] * (LEBAR_TABUNG + JARAK_TABUNG) + JARAK_TABUNG
        self.canvas = tk.Canvas(area, bg=BG_COLOR, highlightthickness=0,
                                 width=lebar_canvas, height=TINGGI_TABUNG + 40)
        self.canvas.place(relx=0.5, rely=0.45, anchor="center")
        self.canvas.bind("<Button-1>", self._saat_klik_canvas)

        # ---------- FOOTER (tombol Urungkan & Ulangi Level) ----------
        footer = tk.Frame(self, bg=BG_COLOR)
        footer.pack(side="bottom", pady=24)

        self.btn_undo = tk.Button(
            footer, text="\u21B6  Urungkan", font=self.font_tombol,
            bg=CARD_COLOR, fg=PRIMARY_BLUE, activebackground="#E8ECFB",
            relief="solid", bd=1, padx=16, pady=8, cursor="hand2",
            command=self._saat_undo,
        )
        self.btn_undo.pack(side="left", padx=8)

        btn_reset = tk.Button(
            footer, text="\u21BB  Ulangi Level", font=self.font_tombol,
            bg=PRIMARY_BLUE, fg="white", activebackground=PRIMARY_BLUE_DARK,
            relief="flat", bd=0, padx=16, pady=8, cursor="hand2",
            command=self._saat_reset_level,
        )
        btn_reset.pack(side="left", padx=8)

    # ------------------------------------------------------------------
    # Menggambar papan (tabung + bola) di Canvas
    # ------------------------------------------------------------------
    def _gambar_papan(self):
        self.canvas.delete("all")
        n_tabung = self.level_data["jumlah_tabung"]

        for i in range(n_tabung):
            x0 = JARAK_TABUNG + i * (LEBAR_TABUNG + JARAK_TABUNG)
            y0 = 10
            x1 = x0 + LEBAR_TABUNG
            y1 = y0 + TINGGI_TABUNG

            outline_color = "#FBBF24" if i == self.tabung_terpilih else "#D8DCF5"
            outline_width = 3 if i == self.tabung_terpilih else 2

            self._gambar_kapsul(x0, y0, x1, y1, outline_color, outline_width)

            # gambar bola dari bawah tabung ke atas
            isi = self.papan[i]
            for pos, warna_id in enumerate(isi):
                cx = (x0 + x1) / 2
                cy = y1 - 20 - pos * (RADIUS_BOLA * 2 + 4)
                warna = WARNA_BOLA[warna_id % len(WARNA_BOLA)]
                self.canvas.create_oval(
                    cx - RADIUS_BOLA, cy - RADIUS_BOLA,
                    cx + RADIUS_BOLA, cy + RADIUS_BOLA,
                    fill=warna, outline="",
                )

    def _gambar_kapsul(self, x0, y0, x1, y1, outline_color, outline_width):
        """Menggambar bentuk tabung (kapsul rounded) memakai kombinasi arc & line."""
        r = (x1 - x0) / 2
        self.canvas.create_arc(x0, y1 - 2 * r, x1, y1, start=180, extent=180,
                                style="arc", outline=outline_color, width=outline_width)
        self.canvas.create_line(x0, y0, x0, y1 - r, fill=outline_color, width=outline_width)
        self.canvas.create_line(x1, y0, x1, y1 - r, fill=outline_color, width=outline_width)

    # ------------------------------------------------------------------
    # Interaksi klik tabung
    # ------------------------------------------------------------------
    def _saat_klik_canvas(self, event):
        if self.selesai:
            return

        n_tabung = self.level_data["jumlah_tabung"]
        for i in range(n_tabung):
            x0 = JARAK_TABUNG + i * (LEBAR_TABUNG + JARAK_TABUNG)
            x1 = x0 + LEBAR_TABUNG
            if x0 <= event.x <= x1:
                self._pilih_tabung(i)
                return

    def _pilih_tabung(self, index_tabung: int):
        if self.tabung_terpilih is None:
            # pilih tabung sumber, hanya jika tidak kosong
            if self.papan[index_tabung]:
                self.tabung_terpilih = index_tabung
                self._gambar_papan()
        else:
            if index_tabung == self.tabung_terpilih:
                # klik tabung yang sama -> batalkan seleksi
                self.tabung_terpilih = None
                self._gambar_papan()
                return

            berhasil = self._coba_pindah(self.tabung_terpilih, index_tabung)
            self.tabung_terpilih = None
            self._gambar_papan()

            if berhasil and self._cek_menang():
                self._saat_menang()

    def _coba_pindah(self, sumber: int, tujuan: int) -> bool:
        """
        Validasi & eksekusi pemindahan bola sesuai aturan (laporan BAB 2.1):
        - bola hanya dari posisi teratas tabung sumber
        - hanya ke tabung kosong ATAU tabung dengan warna teratas sama
        - jika tidak valid, seleksi dibatalkan otomatis (tidak ada perubahan papan)
        """
        tabung_sumber = self.papan[sumber]
        tabung_tujuan = self.papan[tujuan]

        if not tabung_sumber:
            return False
        if len(tabung_tujuan) >= KAPASITAS_TABUNG:
            return False
        if tabung_tujuan and tabung_tujuan[-1] != tabung_sumber[-1]:
            return False

        # simpan state SEBELUM berubah, untuk fitur undo
        self.undo_manager.simpan_state(self.papan)

        bola = tabung_sumber.pop()
        tabung_tujuan.append(bola)
        return True

    def _cek_menang(self) -> bool:
        """Level selesai jika setiap tabung hanya berisi 1 warna atau kosong."""
        for tabung in self.papan:
            if not tabung:
                continue
            if len(set(tabung)) > 1:
                return False
            if len(tabung) != KAPASITAS_TABUNG:
                return False
        return True

    # ------------------------------------------------------------------
    # Undo & Reset
    # ------------------------------------------------------------------
    def _saat_undo(self):
        if self.selesai:
            return
        state_sebelumnya = self.undo_manager.undo()
        if state_sebelumnya is not None:
            self.papan = state_sebelumnya
            self.tabung_terpilih = None
            self._gambar_papan()
        # tidak mempengaruhi timer maupun skor dasar (sesuai laporan 5.4)

    def _saat_reset_level(self):
        self.timer_manager.reset()
        self.timer_manager.mulai()
        self.undo_manager.reset()
        self.papan = generate_board(self.level_data["jumlah_warna"], self.level_data["jumlah_tabung"])
        self.tabung_terpilih = None
        self.selesai = False
        self.label_waktu.config(text=self.timer_manager.get_format_waktu())
        self._gambar_papan()
        # skor TIDAK disimpan saat reset (sesuai laporan 5.5)

    # ------------------------------------------------------------------
    # Timer callbacks
    # ------------------------------------------------------------------
    def _update_label_waktu(self, sisa_waktu: int):
        self.label_waktu.config(text=self.timer_manager.get_format_waktu())

    def _saat_waktu_habis(self):
        self.selesai = True
        self.controller.show_frame(
            "ResultScreen",
            mode="game_over",
            level_data=self.level_data,
        )

    # ------------------------------------------------------------------
    # Kondisi menang -> hitung skor, simpan ke DB, pindah ke Victory Screen
    # ------------------------------------------------------------------
    def _saat_menang(self):
        self.selesai = True
        self.timer_manager.berhenti()

        sisa_waktu = self.timer_manager.get_sisa_waktu()
        rincian_skor = self.score_manager.hitung_skor_level(
            skor_dasar=self.level_data["skor_dasar"],
            sisa_waktu=sisa_waktu,
        )
        self.score_manager.tambah_skor(rincian_skor)
        self.label_skor.config(text=str(rincian_skor["total_skor"]))

        self.score_manager.simpan_skor_ke_database(
            user_id=self.user_id,
            level_reached=self.level_data["nama_level"],
        )

        self.controller.show_frame(
            "ResultScreen",
            mode="victory",
            level_data=self.level_data,
            rincian_skor=rincian_skor,
        )

    def _ke_menu_utama(self):
        self.timer_manager.berhenti()
        self.controller.show_frame("MenuScreen")
