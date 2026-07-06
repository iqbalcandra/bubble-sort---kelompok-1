"""
screens/game_screen.py
Layar permainan utama (generic untuk semua level: Mudah/Sedang/Sulit).

Menggambar tabung & bola pakai Canvas, sesuai desain UI:
- Header: tombol home, judul, badge "Nama Level - Level X", WAKTU, SKOR, gear settings
- Area permainan: tabung digambar sebagai kapsul rounded, bola sebagai lingkaran
- Footer: tombol "Urungkan" (undo) & "Ulangi Level" (reset)

Terhubung ke:
- logic/timer_manager.py  -> countdown & tampilan WAKTU
- logic/score_manager.py  -> hitung skor saat menang
- logic/undo_manager.py   -> fitur urungkan 1 langkah
"""

import tkinter as tk
from tkinter import font as tkfont

from logic.timer_manager import TimerManager
from logic.score_manager import ScoreManager
from logic.undo_manager import UndoManager
from logic.game_logic import generate_board, validasi_pindah, pindah_bola, cek_menang


# ---------------------------------------------------------------------------
# Palet warna & konfigurasi visual (disesuaikan dengan desain Figma)
# ---------------------------------------------------------------------------
BG_COLOR = "#F1F2FB"          # background lavender muda
CARD_COLOR = "#FFFFFF"
AREA_CARD_COLOR = "#D9D9D9"   # card abu-abu pembungkus tabung, sesuai desain baru
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

# Ukuran window aplikasi FIXED (tidak bisa di-resize), sesuai desain UI/UX
LEBAR_WINDOW = 1440
TINGGI_WINDOW = 1024

LEBAR_TABUNG = 96          # diperbesar menyesuaikan window 1440x1024
TINGGI_TABUNG = 380
JARAK_TABUNG = 34
RADIUS_BOLA = 34


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
        super().__init__(master, bg=BG_COLOR, width=LEBAR_WINDOW, height=TINGGI_WINDOW)
        self.controller = controller
        self.level_data = level_data
        self.user_id = user_id
        self.pack_propagate(False)  # kunci ukuran frame, tidak menyusut mengikuti isi

        self.font_judul = tkfont.Font(family="Segoe UI", size=13, weight="bold")
        self.font_badge = tkfont.Font(family="Segoe UI", size=8, weight="bold")
        self.font_label = tkfont.Font(family="Segoe UI", size=9, weight="bold")
        self.font_angka = tkfont.Font(family="Segoe UI", size=13, weight="bold")
        self.font_tombol = tkfont.Font(family="Segoe UI", size=11, weight="bold")

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
        header = tk.Frame(self, bg=CARD_COLOR, height=64)
        header.pack(side="top", fill="x")
        header.pack_propagate(False)

        btn_home = tk.Button(
            header, text="\u2302", font=("Segoe UI", 12), bg="#EEF0FB", fg=PRIMARY_BLUE,
            relief="flat", bd=0, width=3, cursor="hand2",
            command=self._ke_menu_utama,
        )
        btn_home.pack(side="left", padx=(20, 8), pady=14)

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

        btn_gear = tk.Label(header, text="\u2699", font=("Segoe UI", 16),
                             bg="#EEF0FB", fg=PRIMARY_BLUE, padx=12, pady=8)
        btn_gear.pack(side="right", padx=28)

        # ---------- AREA PERMAINAN (CARD ABU-ABU + CANVAS) ----------
        area = tk.Frame(self, bg=BG_COLOR, width=LEBAR_WINDOW, height=TINGGI_WINDOW - 64 - 140)
        area.pack(side="top", fill="both", expand=True)
        area.pack_propagate(False)

        # Card abu-abu muda pembungkus tabung, sesuai desain (dengan margin dari tepi)
        card = tk.Frame(area, bg=AREA_CARD_COLOR)
        card.place(relx=0.5, rely=0.5, anchor="center",
                   width=LEBAR_WINDOW - 80, height=TINGGI_WINDOW - 64 - 140 - 40)

        lebar_canvas = self.level_data["jumlah_tabung"] * (LEBAR_TABUNG + JARAK_TABUNG) + JARAK_TABUNG
        self.canvas = tk.Canvas(card, bg=AREA_CARD_COLOR, highlightthickness=0,
                                 width=lebar_canvas, height=TINGGI_TABUNG + 40)
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")
        self.canvas.bind("<Button-1>", self._saat_klik_canvas)

        # ---------- FOOTER (tombol Urungkan & Ulangi Level) ----------
        footer = tk.Frame(self, bg=BG_COLOR, height=140)
        footer.pack(side="bottom", fill="x", pady=20)
        footer.pack_propagate(False)

        tombol_wrap = tk.Frame(footer, bg=BG_COLOR)
        tombol_wrap.place(relx=0.5, rely=0.5, anchor="center")

        self.btn_undo = tk.Button(
            tombol_wrap, text="\u21B6  Urungkan", font=self.font_tombol,
            bg=CARD_COLOR, fg=PRIMARY_BLUE, activebackground="#E8ECFB",
            relief="solid", bd=1, padx=22, pady=12, cursor="hand2",
            command=self._saat_undo,
        )
        self.btn_undo.pack(side="left", padx=10)

        btn_reset = tk.Button(
            tombol_wrap, text="\u21BB  Ulangi Level", font=self.font_tombol,
            bg=PRIMARY_BLUE, fg="white", activebackground=PRIMARY_BLUE_DARK,
            relief="flat", bd=0, padx=22, pady=12, cursor="hand2",
            command=self._saat_reset_level,
        )
        btn_reset.pack(side="left", padx=10)

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

            outline_color = "#FBBF24" if i == self.tabung_terpilih else "#FFFFFF"
            outline_width = 3 if i == self.tabung_terpilih else 2

            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline=outline_color, width=outline_width, fill=""
            )

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

            sumber = self.tabung_terpilih
            tujuan = index_tabung

            berhasil = False
            if validasi_pindah(self.papan, sumber, tujuan):
                # simpan state SEBELUM berubah, untuk fitur undo
                self.undo_manager.simpan_state(self.papan)
                berhasil = pindah_bola(self.papan, sumber, tujuan)

            self.tabung_terpilih = None
            self._gambar_papan()

            if berhasil and cek_menang(self.papan):
                self._saat_menang()

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
