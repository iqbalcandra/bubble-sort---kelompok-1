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



class GameScreen(tk.Frame):


    def __init__(
            self,
            parent,
            user_data,
            level_data,
            on_back=None
    ):


        super().__init__(
            parent,
            bg="#F8F9FF"
        )


        # ==========================
        # DATA USER & LEVEL
        # ==========================

        self.user_data = user_data

        self.level_data = level_data

        self.on_back = on_back



        # ==========================
        # INISIALISASI MANAGER
        # ==========================

        self.game_logic = GameLogic()

        self.level_manager = LevelManager()

        self.timer_manager = TimerManager()

        self.undo_manager = UndoManager()

        self.score_manager = ScoreManager()

        self.progress_manager = ProgressManager()



        # ==========================
        # DATA GAME
        # ==========================

        self.selected_tube = None


        self.tubes = []


        self.colors = []



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



    # =================================================
    # HEADER
    # =================================================

    def create_header(self):


        header = tk.Frame(
            self,
            bg="#F8F9FF"
        )

        header.pack(
            fill="x",
            pady=20,
            padx=30
        )


        self.title_label = tk.Label(
            header,
            text=f"Color Ball Sort Puzzle - Level {self.level_data['nama_level']}",
            font=("Arial",18,"bold"),
            bg="#F8F9FF",
            fg="#202124"
        )

        self.title_label.pack(
            side="left"
        )



        self.timer_label = tk.Label(
            header,
            text="02:00",
            font=("Arial",16,"bold"),
            bg="#F8F9FF",
            fg="#2170E4"
        )

        self.timer_label.pack(
            side="right",
            padx=20
        )



        self.score_label = tk.Label(
            header,
            text="Score : 0",
            font=("Arial",14,"bold"),
            bg="#F8F9FF",
            fg="#202124"
        )

        self.score_label.pack(
            side="right"
        )



    # =================================================
    # TOOLBAR
    # =================================================

    def create_toolbar(self):


        toolbar = tk.Frame(
            self,
            bg="#F8F9FF"
        )


        toolbar.pack(
            fill="x",
            padx=30,
            pady=10
        )



        self.undo_button = tk.Button(
            toolbar,
            text="↶ Undo",
            width=12,
            font=("Arial",10,"bold"),
            command=self.undo_move
        )

        self.undo_button.pack(
            side="left",
            padx=5
        )



        self.reset_button = tk.Button(
            toolbar,
            text="⟳ Reset",
            width=12,
            font=("Arial",10,"bold"),
            command=self.reset_level
        )

        self.reset_button.pack(
            side="left",
            padx=5
        )



        self.back_button = tk.Button(
            toolbar,
            text="← Menu",
            width=12,
            font=("Arial",10,"bold"),
            command=self.back_menu
        )

        self.back_button.pack(
            side="right"
        )



    # =================================================
    # AREA GAME CANVAS
    # =================================================

    def create_game_area(self):


        self.canvas = tk.Canvas(
            self,
            width=1200,
            height=650,
            bg="#FFFFFF",
            highlightthickness=0
        )


        self.canvas.pack(
            expand=True,
            pady=20
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


        jarak = 130


        posisi_awal = (
            600 -
            ((jumlah_tabung - 1) * jarak) / 2
        )



        for index, tube in enumerate(self.tubes):


            x = (
                posisi_awal +
                (index * jarak)
            )


            y = 170



            # Kotak tabung

            self.canvas.create_rectangle(

                x - 45,

                y,

                x + 45,

                y + 250,

                outline="#333333",

                width=3,

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

                y + 280,

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



    # =================================================
    # GAMBAR BOLA DALAM TABUNG
    # =================================================

    def draw_balls(
            self,
            tube_index,
            x,
            y
    ):


        tube = self.tubes[tube_index]



        posisi_y = y + 190



        # Bola paling bawah digambar dulu

        for warna in tube:


            self.canvas.create_oval(

                x - 30,

                posisi_y,

                x + 30,

                posisi_y + 50,

                fill=warna,

                outline="#FFFFFF",

                width=2

            )


            posisi_y -= 55



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


        jarak = 130


        posisi_awal = (

            600 -

            ((jumlah - 1) * jarak) / 2

        )


        x = (

            posisi_awal +

            index * jarak

        )


        self.canvas.create_rectangle(

            x - 45,

            170,

            x + 45,

            420,

            outline="#2170E4",

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


            self.draw_tubes()



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



        self.progress_manager.update_progress(

            user_id=self.user_data["id"],

            next_level=level_selanjutnya,

            score=score

        )



    # =================================================
    # GAME OVER
    # =================================================

    def game_over(self):


        self.timer_manager.stop()



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
