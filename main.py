import tkinter as tk

from screens.loginscreen import LoginScreen
from screens.menu_screen import MenuScreen


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Color Ball Sort Puzzle")
        self.geometry("1440x1024")
        self.state("zoomed")
        self.configure(bg="#F5F7FB")

        self.frame = None
        self.user_data = {"id": 1, "username": "Guest"}
        self.level_terakhir = None

        self.show_login()

    def clear_frame(self):
        if self.frame is not None:
            self.frame.destroy()
            self.frame = None

    def _placeholder(self, judul):
        self.clear_frame()
        f = tk.Frame(self, bg="#F5F7FB")
        tk.Label(f, text=judul, font=("Arial", 28, "bold"),
                 bg="#F5F7FB").pack(pady=40)
        tk.Button(f, text="Kembali ke Menu", command=self.show_menu).pack()
        f.pack(fill="both", expand=True)
        self.frame = f

    # ---------------------------------------
    # LOGIN
    # ---------------------------------------
    def show_login(self):
        self.clear_frame()
        self.frame = LoginScreen(self, on_login_success=self._login_berhasil)
        self.frame.pack(fill="both", expand=True)

    def _login_berhasil(self, user_data):
        self.user_data = user_data
        self.show_menu()

    # ---------------------------------------
    # MENU
    # ---------------------------------------
    def show_menu(self):
        self.clear_frame()
        self.frame = MenuScreen(
            self,
            on_mulai=self.show_pilih_level,
            on_leaderboard=self.show_leaderboard,
            on_progress=self.show_progress,
            on_logout=self.show_login,
        )
        self.frame.pack(fill="both", expand=True)

    # ---------------------------------------
    # PILIH LEVEL
    # ---------------------------------------
    def show_pilih_level(self):
        self.clear_frame()
        try:
            from screens.level_screen import LevelScreen
            self.frame = LevelScreen(
                self,
                self.user_data,
                on_pilih_level=self._klik_pilih_level,
                on_kembali=self.show_menu,
            )
            self.frame.pack(fill="both", expand=True)
        except Exception as e:
            print(e)
            self._placeholder("Pilih Level")

    def _klik_pilih_level(self, level_data):
        self.show_game(level_data)

    # ---------------------------------------
    # GAME
    # ---------------------------------------
    def show_game(self, level_data=None):
        self.clear_frame()

        if level_data is None:
            level_data = self.level_terakhir or {
                "id_level": 1,
                "nama_level": "Mudah",
                "jumlah_warna": 4,
                "jumlah_tabung": 6,
                "timer": 120,
            }

        self.level_terakhir = level_data

        try:
            from screens.game_screen import GameScreen
            self.frame = GameScreen(
                self,
                self.user_data,
                level_data,
                on_back=self.show_menu,
                on_menang=self.show_level_selesai,
                on_kalah=self.show_game_over,
            )
            self.frame.pack(fill="both", expand=True)
        except Exception as e:
            print(e)
            self._placeholder("Game Screen")

    # ---------------------------------------
    # LEVEL SELESAI
    # ---------------------------------------
    def show_level_selesai(self, level_data=None, rincian_skor=None, ada_lanjut=True):
        self.clear_frame()

        level_data = level_data or self.level_terakhir
        rincian_skor = rincian_skor or {}
        skor_dasar = rincian_skor.get("skor_dasar", 200)
        bonus_waktu = rincian_skor.get("bonus_waktu", 0)

        try:
            from screens.levelselesai import LevelSelesaiScreen
            self.frame = LevelSelesaiScreen(
                self,
                skor_dasar=skor_dasar,
                bonus_waktu=bonus_waktu,
                on_level_berikutnya=(
                    self.show_pilih_level if ada_lanjut else self.show_menu),
                on_ulangi=lambda: self.show_game(level_data),
                on_kembali=self.show_menu,
            )
            self.frame.pack(fill="both", expand=True)
        except Exception as e:
            print(e)
            self._placeholder("Level Selesai")

    # ---------------------------------------
    # GAME OVER
    # ---------------------------------------
    def show_game_over(self, level_data=None):
        self.clear_frame()
        level_data = level_data or self.level_terakhir

        try:
            from screens.gameover import GameOverScreen
            self.frame = GameOverScreen(
                self,
                on_retry=lambda: self.show_game(level_data),
                on_menu=self.show_menu,
            )
            self.frame.pack(fill="both", expand=True)
        except Exception as e:
            print(e)
            self._placeholder("Game Over")

    # ---------------------------------------
    # LEADERBOARD
    # ---------------------------------------
    def show_leaderboard(self):
        self.clear_frame()
        try:
            from screens.leaderboard import LeaderboardScreen
            self.frame = LeaderboardScreen(
                self, self.user_data, on_kembali=self.show_menu)
            self.frame.pack(fill="both", expand=True)
        except Exception as e:
            print(e)
            self._placeholder("Leaderboard")

    # ---------------------------------------
    # PROGRESS
    # ---------------------------------------
    def show_progress(self):
        self.clear_frame()
        try:
            from screens.progres import ProgresScreen
            self.frame = ProgresScreen(
                self,
                on_kembali=self.show_menu,
                on_lanjut_bermain=self.show_pilih_level,
            )
            self.frame.pack(fill="both", expand=True)
        except Exception as e:
            print(e)
            self._placeholder("Progress")


if __name__ == "__main__":
    app = App()
    app.mainloop()
