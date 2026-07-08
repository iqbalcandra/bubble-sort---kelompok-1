import tkinter as tk

from screens.loginscreen import LoginScreen
from screens.menu_screen import MenuScreen
from screens.level_screen import LevelScreen


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Color Ball Sort Puzzle")
        self.geometry("1440x1024")
        self.state("zoomed")
        self.minsize(1440, 1024)
        self.resizable(False, False)
        self.configure(bg="#F5F7FB")

        self.user_data = None
        self.frame = None

        self.show_login()

    # ---------------------------------------
    # GANTI HALAMAN
    # ---------------------------------------

    def clear_frame(self):
        if self.frame:
            self.frame.destroy()

    # ---------------------------------------
    # LOGIN
    # ---------------------------------------

    def show_login(self):
        self.clear_frame()

        self.frame = LoginScreen(
            self,
            on_login=self.show_menu
        )

        self.frame.pack(fill="both", expand=True)

    # ---------------------------------------
    # MENU
    # ---------------------------------------

    def show_menu(self, user_data=None):
        self.clear_frame()

        if user_data:
            self.user_data = user_data

        self.frame = MenuScreen(
            self,
            on_mulai=self.show_level,
            on_leaderboard=None,
            on_progress=None,
            on_setting=None,
            on_logout=self.show_login
        )

        self.frame.pack(fill="both", expand=True)

    # ---------------------------------------
    # LEVEL
    # ---------------------------------------

    def show_level(self):
        self.clear_frame()

        self.frame = LevelScreen(
            self,
            user_data=self.user_data,
            on_pilih_level=None,
            on_kembali=self.show_menu
        )

        self.frame.pack(fill="both", expand=True)


# ---------------------------------------
# MENJALANKAN PROGRAM
# ---------------------------------------

if __name__ == "__main__":
    app = App()
    app.mainloop()