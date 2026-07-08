import tkinter as tk

from screens.loginscreen import LoginScreen
from screens.menu_screen import MenuScreen


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Color Ball Sort Puzzle")
        self.geometry("1440x1024")
        self.state("zoomed")
        self.minsize(1440, 1024)
        self.configure(bg="#F5F7FB")

        self.frame = None

        self.show_login()

    # -----------------------------
    # GANTI HALAMAN
    # -----------------------------

    def clear_frame(self):
        if self.frame is not None:
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

        self.frame = MenuScreen(self)
        self.frame.pack(fill="both", expand=True)


# -----------------------------
# MENJALANKAN PROGRAM
# -----------------------------

if __name__ == "__main__":
    app = App()
    app.mainloop()