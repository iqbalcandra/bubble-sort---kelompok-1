import tkinter as tk
from tkinter import messagebox

from screens.loginscreen import LoginScreen
from screens.menu_screen import MenuScreen
from screens.level_screen import LevelScreen
from screens.leaderboard import LeaderboardScreen
from screens.progres import ProgressScreen

# nanti menyusul
# from screens.game_screen import GameScreen
# from screens.levelselesai import LevelSelesaiScreen
# from screens.gameover import GameOverScreen

from theme import (
    LEBAR_WINDOW,
    TINGGI_WINDOW,
    BG_COLOR
)


class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Color Ball Sort Puzzle")
        self.geometry(f"{LEBAR_WINDOW}x{TINGGI_WINDOW}")
        self.state("zoomed")
        self.minsize(LEBAR_WINDOW, TINGGI_WINDOW)

        self.configure(bg=BG_COLOR)
        self.resizable(False, False)

        self.frame = None

        # sementara user dummy
        self.user = {
            "id": 1,
            "username": "Player"
        }

        self.show_login()

    # -----------------------------
    # ganti halaman
    # -----------------------------

    def clear_frame(self):
        if self.frame:
            self.frame.destroy()

                # -----------------------------
    # LOGIN
    # -----------------------------

    def show_login(self):

        self.clear_frame()

        self.frame = LoginScreen(
            self,
            on_login=self.show_menu
        )

        self.frame.pack(fill="both", expand=True)

    # -----------------------------
    # MENU
    # -----------------------------

    def show_menu(self):

        self.clear_frame()

        self.frame = MenuScreen(
            self,
            on_mulai=self.show_level,
            on_leaderboard=self.show_leaderboard,
            on_progress=self.show_progress,
            on_setting=self.show_setting,
            on_logout=self.logout
        )

        self.frame.pack(fill="both", expand=True)

            # -----------------------------
    # LEVEL
    # -----------------------------

    def show_level(self):

        self.clear_frame()

        self.frame = LevelScreen(
            self,
            on_kembali=self.show_menu,
            on_mulai=self.show_game
        )

        self.frame.pack(fill="both", expand=True)

    # -----------------------------
    # GAME
    # -----------------------------

    def show_game(self, level=None):

        self.clear_frame()

        messagebox.showinfo(
            "Info",
            "Game Screen belum dihubungkan."
        )

        # Nanti diganti menjadi:
        #
        # self.frame = GameScreen(
        #     self,
        #     level=level,
        #     on_selesai=self.show_level_selesai,
        #     on_game_over=self.show_game_over
        # )
        #
        # self.frame.pack(fill="both", expand=True)

    # -----------------------------
    # LEADERBOARD
    # -----------------------------

    def show_leaderboard(self):

        self.clear_frame()

        self.frame = LeaderboardScreen(
            self,
            on_kembali=self.show_menu
        )

        self.frame.pack(fill="both", expand=True)

    # -----------------------------
    # PROGRESS
    # -----------------------------

    def show_progress(self):

        self.clear_frame()

        self.frame = ProgressScreen(
            self,
            on_kembali=self.show_menu
        )

        self.frame.pack(fill="both", expand=True)

    # -----------------------------
    # SETTING
    # -----------------------------

    def show_setting(self):

        messagebox.showinfo(
            "Pengaturan",
            "Halaman pengaturan masih dalam pengembangan."
        )

    # -----------------------------
    # LOGOUT
    # -----------------------------

    def logout(self):

        if messagebox.askyesno(
            "Keluar",
            "Apakah ingin kembali ke halaman login?"
        ):
            self.show_login()

# -----------------------------
# MENJALANKAN PROGRAM
# -----------------------------

if __name__ == "__main__":
    app = App()
    app.mainloop()