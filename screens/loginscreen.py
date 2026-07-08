import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk


class LoginScreen:

    def __init__(self):

        # ===============================
        # WINDOW
        # ===============================

        self.root = tk.Tk()
        self.root.title("Color Ball Sort Puzzle")
        self.root.geometry("1100x650")
        self.root.state("zoomed")
        self.root.configure(bg="#F5F5F5")
        self.root.resizable(False, False)

        # ===============================
        # PATH
        # ===============================

        self.BASE_DIR = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))

        # ===============================
        # LOAD GAMBAR
        # ===============================

        logo_path = os.path.join(self.BASE_DIR, "aset", "logo_baru.PNG")

        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((120, 120))

        self.logo = ImageTk.PhotoImage(logo_img)

        # ===============================
        # BUILD UI
        # ===============================

        self._build_main_frame()
        self._build_left_section()
        self._build_right_section()
        self._build_login_card()
        self._build_register_card()

        self.login_card.pack(expand=True)
        self.register_card.pack_forget()

    # ===============================
    # FUNGSI
    # ===============================

    def login(self):

        username = self.login_username.get()
        password = self.login_password.get()

        if username == "" or password == "":
            messagebox.showerror(
                "Error",
                "Username dan Password harus diisi!"
            )
            return

        messagebox.showinfo(
            "Login",
            f"Selamat datang, {username}"
        )

        # Tutup window login
        self.root.destroy()

        # Jalankan menu screen
        menu_path = os.path.join(self.BASE_DIR, "screens", "menu_screen.py")

        subprocess.Popen([sys.executable, menu_path])

    def register(self):

        if self.reg_username.get() == "" \
                or self.reg_password.get() == "" \
                or self.reg_confirm.get() == "":

            messagebox.showerror(
                "Error",
                "Semua data harus diisi!"
            )
            return

        if self.reg_password.get() != self.reg_confirm.get():

            messagebox.showerror(
                "Error",
                "Konfirmasi password tidak cocok!"
            )
            return

        messagebox.showinfo(
            "Berhasil",
            "Registrasi berhasil.\nSilakan login."
        )

        self.show_login()

    def show_login(self):
        self.login_card.pack(expand=True)
        self.register_card.pack_forget()

    def show_register(self):
        self.register_card.pack(expand=True)
        self.login_card.pack_forget()

    def show_login_password(self):

        if self.login_show.get():
            self.login_password.config(show="")
        else:
            self.login_password.config(show="*")

    def show_register_password(self):

        if self.register_show.get():

            self.reg_password.config(show="")
            self.reg_confirm.config(show="")

        else:

            self.reg_password.config(show="*")
            self.reg_confirm.config(show="*")

    # ===============================
    # BUILD UI - HELPER
    # ===============================

    def _build_main_frame(self):

        self.main = tk.Frame(
            self.root,
            bg="#F5F5F5"
        )

        self.main.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=30
        )

    def _build_left_section(self):

        self.left = tk.Frame(
            self.main,
            bg="#F5F5F5"
        )

        self.left.pack(
            side="left",
            fill="both",
            expand=True
        )

        tk.Label(
            self.left,
            image=self.logo,
            bg="#F5F5F5"
        ).pack(
            pady=(120, 20)
        )

        tk.Label(
            self.left,
            text="Color Ball Sort Puzzle",
            font=("Arial", 24, "bold"),
            fg="#1565D8",
            bg="#F5F5F5"
        ).pack()

        tk.Label(
            self.left,
            text="Susun warna, asah logika,\ndan raih skor tertinggi\nbersama teman-temanmu!",
            font=("Arial", 11),
            fg="gray",
            bg="#F5F5F5",
            justify="center"
        ).pack(
            pady=15
        )

    def _build_right_section(self):

        self.right = tk.Frame(
            self.main,
            bg="#F5F5F5"
        )

        self.right.pack(
            side="right",
            fill="both",
            expand=True
        )

    def _build_login_card(self):

        self.login_card = tk.Frame(
            self.right,
            bg="white",
            width=360,
            height=550,
            bd=1,
            relief="solid"
        )

        self.login_card.pack_propagate(False)
        self.login_card.pack(expand=True)

        tk.Label(
            self.login_card,
            image=self.logo,
            bg="white"
        ).pack(pady=(25, 10))

        tk.Label(
            self.login_card,
            text="Color Ball Sort Puzzle",
            font=("Arial", 16, "bold"),
            fg="#1565D8",
            bg="white"
        ).pack()

        tk.Label(
            self.login_card,
            text="Selamat Datang Kembali",
            font=("Arial", 10),
            bg="white",
            fg="gray"
        ).pack(pady=(0, 20))

        # ---------------- Username ----------------

        tk.Label(
            self.login_card,
            text="Username",
            bg="white",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", padx=35)

        self.login_username = tk.Entry(
            self.login_card,
            width=35,
            font=("Arial", 11)
        )

        self.login_username.pack(
            padx=35,
            pady=(5, 15),
            ipady=5
        )

        # ---------------- Password ----------------

        tk.Label(
            self.login_card,
            text="Password",
            bg="white",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", padx=35)

        self.login_password = tk.Entry(
            self.login_card,
            width=35,
            font=("Arial", 11),
            show="*"
        )

        self.login_password.pack(
            padx=35,
            pady=(5, 5),
            ipady=5
        )

        self.login_show = tk.BooleanVar()

        tk.Checkbutton(
            self.login_card,
            text="Tampilkan Password",
            variable=self.login_show,
            command=self.show_login_password,
            bg="white"
        ).pack(
            anchor="w",
            padx=35,
            pady=(0, 20)
        )

        # ---------------- Tombol Login ----------------

        tk.Button(
            self.login_card,
            text="Masuk",
            bg="#1565D8",
            fg="white",
            font=("Arial", 11, "bold"),
            width=28,
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.login
        ).pack()

        # ---------------- Pindah Register ----------------

        frame_bawah = tk.Frame(
            self.login_card,
            bg="white"
        )

        frame_bawah.pack(pady=20)

        tk.Label(
            frame_bawah,
            text="Belum punya akun?",
            bg="white",
            fg="gray"
        ).pack(side="left")

        tk.Button(
            frame_bawah,
            text="Daftar",
            bg="white",
            fg="#1565D8",
            relief="flat",
            cursor="hand2",
            command=self.show_register
        ).pack(side="left")

    def _build_register_card(self):

        self.register_card = tk.Frame(
            self.right,
            bg="white",
            width=360,
            height=550,
            bd=1,
            relief="solid"
        )

        self.register_card.pack_propagate(False)
        self.register_card.pack(expand=True)
        self.register_card.pack_forget()

        tk.Label(
            self.register_card,
            image=self.logo,
            bg="white"
        ).pack(pady=(20, 10))

        tk.Label(
            self.register_card,
            text="Buat Akun Baru",
            font=("Arial", 16, "bold"),
            fg="#1565D8",
            bg="white"
        ).pack()

        tk.Label(
            self.register_card,
            text="Daftar dan mulai petualanganmu!",
            font=("Arial", 10),
            bg="white",
            fg="gray"
        ).pack(pady=(0, 20))

        # ---------- Username ----------

        tk.Label(
            self.register_card,
            text="Username",
            bg="white",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", padx=35)

        self.reg_username = tk.Entry(
            self.register_card,
            width=35,
            font=("Arial", 11)
        )

        self.reg_username.pack(
            padx=35,
            pady=(5, 15),
            ipady=5
        )

        # ---------- Password ----------

        tk.Label(
            self.register_card,
            text="Password",
            bg="white",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", padx=35)

        self.reg_password = tk.Entry(
            self.register_card,
            width=35,
            font=("Arial", 11),
            show="*"
        )

        self.reg_password.pack(
            padx=35,
            pady=(5, 15),
            ipady=5
        )

        # ---------- Konfirmasi Password ----------

        tk.Label(
            self.register_card,
            text="Konfirmasi Password",
            bg="white",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", padx=35)

        self.reg_confirm = tk.Entry(
            self.register_card,
            width=35,
            font=("Arial", 11),
            show="*"
        )

        self.reg_confirm.pack(
            padx=35,
            pady=(5, 5),
            ipady=5
        )

        # ---------- Show Password ----------

        self.register_show = tk.BooleanVar()

        tk.Checkbutton(
            self.register_card,
            text="Tampilkan Password",
            variable=self.register_show,
            command=self.show_register_password,
            bg="white"
        ).pack(
            anchor="w",
            padx=35,
            pady=(0, 20)
        )

        # ---------- Tombol Register ----------

        tk.Button(
            self.register_card,
            text="Daftar",
            bg="#1565D8",
            fg="white",
            font=("Arial", 11, "bold"),
            width=28,
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.register
        ).pack()

        # ---------- Kembali Login ----------

        frame_login = tk.Frame(
            self.register_card,
            bg="white"
        )

        frame_login.pack(pady=20)

        tk.Label(
            frame_login,
            text="Sudah punya akun?",
            bg="white",
            fg="gray"
        ).pack(side="left")

        tk.Button(
            frame_login,
            text="Masuk",
            bg="white",
            fg="#1565D8",
            relief="flat",
            cursor="hand2",
            command=self.show_login
        ).pack(side="left")

    # ===============================
    # RUN
    # ===============================

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = LoginScreen()
    app.run()
