"""
screens/game_screen.py

Halaman utama permainan Color Ball Sort Puzzle.

Tugas:
- Membuat UI Game
- Menggambar tabung
- Menggambar bola
- Menangani klik pemain
- Memanggil logic manager

CATATAN PERBAIKAN:
- generate_tubes(), move_ball(), check_win() DIHAPUS dari file ini (dulu
  duplikat logic manual) -> sekarang dipanggil lewat self.game_logic
  (lihat logic/game_logic.py, class GameLogic).
- Import "logic.progres_manager" diperbaiki jadi "logic.progress_manager"
  (nama file & class yang benar: ProgressManager).
"""

import os
import tkinter as tk
from tkinter import messagebox


# ================================
# IMPORT LOGIC MANAGER
# ================================

from logic.game_logic import GameLogic
from logic.level_manager import LevelManager
from logic.score_manager import ScoreManager
from logic.timer_manager import TimerManager
from logic.undo_manager import UndoManager
from logic.progres_manager import ProgressManager
from theme import BG_COLOR, CARD_COLOR, PRIMARY_BLUE, TEXT_DARK


class GameScreen(tk.Frame):

    def __init__(
            self,
            parent,
            user_data,
            level_data,
            on_back=None,
            on_menang=None,
            on_kalah=None
    ):

        super().__init__(
            parent,
            bg=BG_COLOR
        )

        # ==========================
        # DATA USER & LEVEL
        # ==========================

        self.user_data = user_data

        self.level_data = level_data

        self.on_back = on_back

        self.on_menang = on_menang

        self.on_kalah = on_kalah

        # ==========================
        # INISIALISASI MANAGER
        # ==========================

        self.game_logic = GameLogic()

        self.level_manager = LevelManager()

        self.timer_manager = TimerManager()

        self.undo_manager = UndoManager()

        self.score_manager = ScoreManager()

        self.progres_manager = ProgressManager()

        # ==========================
        # DATA GAME
        # ==========================

        self.selected_tube = None

        self.tubes = []

        self.colors = []

        self.images = {}

        self.load_assets()

        # ==========================
        # BUILD UI
        # ==========================

        self.create_header()

        self.create_toolbar()

        self.create_game_area()

        # ==========================
        # MULAI LEVEL
        # ==========================

        self.start_level()

    def load_assets(self):

        base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        folder_game = os.path.join(
            base_dir,
            "aset",
            "Gambar dan icon halaman permainan"
        )

        print("======================")
        print("CEK ASSET GAME")
        print(folder_game)
        print("======================")

        def load(nama):

            path = os.path.join(
                folder_game,
                nama
            )

            if os.path.exists(path):

                print("BERHASIL :", nama)

                return tk.PhotoImage(
                    file=path
                )

            else:

                print("TIDAK DITEMUKAN :", nama)

                return None

        self.images["merah"] = load(
            "Bola_merah.png"
        )

        self.images["biru"] = load(
            "Bola_biru.png"
        )

        self.images["kuning"] = load(
            "Bola_kuning.png"
        )

        self.images["tabung"] = load(
            "Tabung.png"
        )

        self.images["timer"] = load(
            "Icon Timer.png"
        )

        self.images["score"] = load(
            "Icon Score.png"
        )

        self.images["undo"] = load(
            "Icon Undo.png"
        )

        self.images["reset"] = load(
            "Icon Reset.png"
        )

        self.images["menu"] = load(
            "Icon Menu.png"
        )

        print("SELESAI LOAD ASSET")

    # =================================================
    # HEADER
    # =================================================

    def create_header(self):

        header = tk.Frame(
            self,
            bg=BG_COLOR
        )

        header.pack(
            fill="x",
            pady=20,
            padx=30
        )

        # ==========================
        # JUDUL GAME
        # ==========================

        self.title_label = tk.Label(
            header,
            text=f"Color Ball Sort Puzzle - Level {self.level_data['nama_level']}",
            font=("Arial", 18, "bold"),
            bg=BG_COLOR,
            fg=TEXT_DARK
        )

        self.title_label.pack(
            side="left"
        )

        # ==========================
        # AREA SCORE
        # ==========================

        score_frame = tk.Frame(
            header,
            bg=BG_COLOR
        )

        score_frame.pack(
            side="right",
            padx=20
        )

        tk.Label(
            score_frame,
            image=self.images.get("score"),
            bg=BG_COLOR
        ).pack(
            side="left"
        )

        self.score_label = tk.Label(
            score_frame,
            text="0",
            font=("Arial", 14, "bold"),
            bg=BG_COLOR,
            fg=TEXT_DARK
        )

        self.score_label.pack(
            side="left",
            padx=5
        )

        # ==========================
        # AREA TIMER
        # ==========================

        timer_frame = tk.Frame(
            header,
            bg=BG_COLOR
        )

        timer_frame.pack(
            side="right",
            padx=20
        )

        tk.Label(
            timer_frame,
            image=self.images.get("timer"),
            bg=BG_COLOR
        ).pack(
            side="left"
        )

        self.timer_label = tk.Label(
            timer_frame,
            text="02:00",
            font=("Arial", 16, "bold"),
            bg=BG_COLOR,
            fg=PRIMARY_BLUE
        )

        self.timer_label.pack(
            side="left",
            padx=5
        )
    # =================================================
    # TOOLBAR
    # =================================================

    def create_toolbar(self):

        toolbar = tk.Frame(
            self,
            bg=BG_COLOR
        )

        toolbar.pack(
            fill="x",
            padx=30,
            pady=10
        )

        self.undo_button = tk.Button(
            toolbar,
            image=self.images.get("undo"),
            compound="left",
            text="Undo",
            font=("Arial", 10, "bold"),
            command=self.undo_move
        )

        self.undo_button.pack(
            side="left",
            padx=5
        )

        self.reset_button = tk.Button(
            toolbar,
            image=self.images.get("reset"),
            compound="left",
            text="Reset",
            font=("Arial", 10, "bold"),
            command=self.reset_level
        )

        self.reset_button.pack(
            side="left",
            padx=5
        )

        self.back_button = tk.Button(
            toolbar,
            image=self.images.get("menu"),
            compound="left",
            text="Menu",
            font=("Arial", 10, "bold"),
            command=self.back_menu
        )

        self.back_button.pack(
            side="right"
        )

    # =================================================
    # AREA GAME CANVAS
    # =================================================

    def create_game_area(self):

        # Card abu-abu pembungkus tabung, biar lebih dekat ke desain Figma
        # (dulu tabung langsung nempel background utama tanpa wadah)
        area_card = tk.Frame(
            self,
            bg="#D9D9D9"
        )

        area_card.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=(0, 20)
        )

        self.canvas = tk.Canvas(
            area_card,
            width=1360,
            height=680,
            bg="#D9D9D9",
            highlightthickness=0
        )

        self.canvas.pack(
            expand=True
        )

    # =================================================
    # START LEVEL
    # =================================================

    def start_level(self):

        jumlah_warna = self.level_data["jumlah_warna"]

        jumlah_tabung = self.level_data["jumlah_tabung"]

        # Membuat susunan bola awal (dipindah ke logic/game_logic.py)
        self.tubes = self.game_logic.generate_tubes(
            jumlah_warna,
            jumlah_tabung
        )

        # Set skor berdasarkan level
        self.score_manager.set_level(
            self.level_data
        )

        # Mulai timer
        self.timer_manager.start(
            self.level_data["timer"]
        )

        # Tampilkan game
        self.draw_tubes()

        # Jalankan update timer
        self.update_timer()

    # =================================================
    # GAMBAR SEMUA TABUNG
    # =================================================

    def draw_tubes(self):

        self.canvas.delete(
            "all"
        )

        jumlah_tabung = len(
            self.tubes
        )

        jarak = 150

        posisi_awal = (
            680 -
            ((jumlah_tabung - 1) * jarak) / 2
        )

        for index, tube in enumerate(self.tubes):

            x = (
                posisi_awal +
                (index * jarak)
            )

            y = 170

            # Kotak tabung

            self.canvas.create_image(
                x,
                y + 150,
                image=self.images["tabung"],
                tags=f"tube_{index}"
            )

            # Gambar bola

            self.draw_balls(

                index,

                x,

                y

            )

            # Nomor tabung

            self.canvas.create_text(

                x,

                y + 330,

                text=f"{index+1}",

                font=(
                    "Arial",
                    12,
                    "bold"
                )

            )

            # Event klik tabung

            self.canvas.tag_bind(

                f"tube_{index}",

                "<Button-1>",

                lambda event, i=index:
                self.click_tube(i)

            )

        # Gambar ulang highlight tabung terpilih (jika ada), supaya tetap
        # terlihat setelah canvas di-clear & digambar ulang.
        if self.selected_tube is not None:
            self.highlight_tube(self.selected_tube)

    def draw_balls(self, tube_index, x, y):

        tube = self.tubes[tube_index]

        posisi_y = y + 220

        for warna in tube:

            if warna == "#FF5252":
                gambar = self.images["merah"]

            elif warna == "#2196F3":
                gambar = self.images["biru"]

            elif warna == "#FFC107":
                gambar = self.images["kuning"]

            else:
                gambar = None

            if gambar:
                self.canvas.create_image(
                    x,
                    posisi_y,
                    image=gambar,
                    tags=f"tube_{tube_index}"
                )
            else:
                # fallback kalau warna tidak ada gambarnya
                self.canvas.create_oval(
                    x-30,
                    posisi_y-30,
                    x+30,
                    posisi_y+30,
                    fill=warna,
                    outline="white",
                    tags=f"tube_{tube_index}"
                )

            posisi_y -= 68
    # =================================================
    # KLIK TABUNG
    # =================================================

    def click_tube(self, index):

        # Jika belum ada tabung dipilih
        if self.selected_tube is None:

            # Tidak bisa pilih tabung kosong

            if len(self.tubes[index]) == 0:

                return

            self.selected_tube = index

            self.highlight_tube(index)

        else:

            sumber = self.selected_tube

            tujuan = index

            # Klik tabung yang sama
            if sumber == tujuan:

                self.selected_tube = None

                self.draw_tubes()

                return

            # Simpan state SEBELUM pindah, hanya jika langkahnya valid
            # (supaya undo tidak menyimpan state yang identik / percuma)
            berhasil = False

            if self.game_logic.validasi_pindah(self.tubes, sumber, tujuan):

                self.undo_manager.save_state(self.tubes)

                berhasil = self.game_logic.move_ball(
                    self.tubes,
                    sumber,
                    tujuan
                )

            self.selected_tube = None

            self.draw_tubes()

            # cek menang

            if berhasil and self.game_logic.check_win(self.tubes):

                self.win_game()

    # =================================================
    # HIGHLIGHT TABUNG TERPILIH
    # =================================================

    def highlight_tube(self, index):

        # menggambar border highlight di atas tabung yang dipilih
        # (koordinat disamakan persis dengan kotak tabung di draw_tubes:
        #  x-45..x+45, y 170..420)

        jumlah = len(self.tubes)

        jarak = 150

        posisi_awal = (

            680 -

            ((jumlah - 1) * jarak) / 2

        )

        x = (

            posisi_awal +

            index * jarak

        )

        self.canvas.create_rectangle(

            x - 55,

            170,

            x + 55,

            470,

            outline=PRIMARY_BLUE,

            width=5,

            tags="highlight"

        )

    # =================================================
    # UNDO
    # =================================================

    def undo_move(self):

        state = self.undo_manager.undo()

        if state:

            self.tubes = state

            self.selected_tube = None

            self.draw_tubes()

        else:

            messagebox.showinfo(
                "Undo",
                "Belum ada langkah yang bisa dikembalikan."
            )

    # =================================================
    # RESET LEVEL
    # =================================================

    def reset_level(self):

        jawaban = messagebox.askyesno(

            "Reset",

            "Yakin ingin mengulang level?"

        )

        if not jawaban:

            return

        self.timer_manager.stop()

        self.undo_manager.clear()

        self.selected_tube = None

        self.start_level()

    # =================================================
    # UPDATE TIMER
    # =================================================

    def update_timer(self):

        self.timer_label.config(

            text=self.timer_manager.get_format_time()

        )

        if self.timer_manager.is_habis():

            self.game_over()

            return

        # update setiap 1 detik

        self.after(

            1000,

            self.update_timer

        )

    # =================================================
    # MENANG
    # =================================================

    def win_game(self):

        # hentikan timer

        self.timer_manager.stop()

        # ambil sisa waktu

        sisa_waktu = (

            self.timer_manager.get_sisa_waktu()

        )

        # hitung skor

        total_score = (

            self.score_manager.hitung_skor(

                sisa_waktu

            )

        )

        self.score_label.config(

            text=f"Score : {total_score}"

        )

        # simpan skor database

        self.score_manager.simpan_skor(

            self.user_data["id"],

            self.level_data["nama_level"]

        )

        # update progress

        self.update_player_progress(
            total_score
        )

        # tampilkan Victory Screen (levelselesai.py) lewat callback,
        # atau fallback messagebox kalau main.py belum menyambungkan on_menang
        if self.on_menang:

            rincian_skor = self.score_manager.get_rincian_skor()

            ada_lanjut = not self.level_manager.is_level_terakhir(
                self.level_data["id_level"]
            )

            self.on_menang(self.level_data, rincian_skor, ada_lanjut)

        else:

            messagebox.showinfo(

                "Level Selesai",

                f"""
Selamat!

Level :
{self.level_data['nama_level']}

Skor :
{total_score}

Bonus Waktu :
{sisa_waktu * 10}
"""

            )

    # =================================================
    # UPDATE PROGRESS PLAYER
    # =================================================

    def update_player_progress(
            self,
            score
    ):

        next_level = (

            self.level_manager.next_level(

                self.level_data["id_level"]

            )

        )

        if next_level:

            level_selanjutnya = (

                next_level["nama_level"]

            )

        else:

            level_selanjutnya = (

                self.level_data["nama_level"]

            )

        self.progres_manager.update_progress(

            user_id=self.user_data["id"],

            next_level=level_selanjutnya,

            score=score

        )

    # =================================================
    # GAME OVER
    # =================================================

    def game_over(self):

        self.timer_manager.stop()

        # tampilkan Game Over Screen (gameover.py) lewat callback,
        # atau fallback messagebox + auto reset kalau main.py belum
        # menyambungkan on_kalah
        if self.on_kalah:

            self.on_kalah(self.level_data)

        else:

            messagebox.showwarning(

                "Game Over",

                f"""
Waktu Habis!

Level :
{self.level_data['nama_level']}

Coba lagi untuk menyelesaikan puzzle.
"""

            )

            self.reset_level()

    # =================================================
    # KEMBALI KE MENU
    # =================================================

    def back_menu(self):

        jawaban = messagebox.askyesno(

            "Kembali",

            "Keluar dari permainan?"

        )

        if not jawaban:

            return

        self.timer_manager.stop()

        if self.on_back:

            self.on_back()
