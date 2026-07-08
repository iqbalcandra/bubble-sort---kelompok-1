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
        self.frame=None
        self.show_login()

    # ---------------------------------------
    # GANTI HALAMAN
    # ---------------------------------------
    def clear_frame(self):
        if self.frame is not None:
            self.frame.destroy()

    # ---------------------------------------
    # LOGIN
    # ---------------------------------------
    def show_login(self):
        self.clear_frame()
        self.frame=LoginScreen(self,on_login=self.show_menu)
        self.frame.pack(fill="both",expand=True)

    # ---------------------------------------
    # MENU
    # ---------------------------------------
    def show_menu(self):
        self.clear_frame()
        self.frame=MenuScreen(
            self,
            on_mulai=self.show_game,
            on_leaderboard=self.show_leaderboard,
            on_progress=self.show_progress,
            on_setting=self.show_setting,
            on_logout=self.show_login
        )
        self.frame.pack(fill="both",expand=True)

    def _placeholder(self,judul):
        self.clear_frame()
        f=tk.Frame(self,bg="#F5F7FB")
        tk.Label(f,text=judul,font=("Arial",28,"bold"),bg="#F5F7FB").pack(pady=40)
        tk.Button(f,text="Kembali ke Menu",command=self.show_menu).pack()
        f.pack(fill="both",expand=True)
        self.frame=f

    def show_game(self):
        try:
            from screens.game_screen import GameScreen
            self.clear_frame()
            self.frame=GameScreen(self)
            self.frame.pack(fill="both",expand=True)
        except Exception:
            self._placeholder("Game Screen")

    def show_leaderboard(self):
        try:
            from screens.leaderboard_screen import LeaderboardScreen
            self.clear_frame()
            self.frame=LeaderboardScreen(self)
            self.frame.pack(fill="both",expand=True)
        except Exception:
            self._placeholder("Leaderboard")

    def show_progress(self):
        try:
            from screens.progress_screen import ProgressScreen
            self.clear_frame()
            self.frame=ProgressScreen(self)
            self.frame.pack(fill="both",expand=True)
        except Exception:
            self._placeholder("Progress")

    def show_setting(self):
        try:
            from screens.setting_screen import SettingScreen
            self.clear_frame()
            self.frame=SettingScreen(self)
            self.frame.pack(fill="both",expand=True)
        except Exception:
            self._placeholder("Setting")


if __name__=="__main__":
    app=App()
    app.mainloop()
