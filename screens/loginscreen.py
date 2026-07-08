"""
screens/login_screen.py

Halaman Login & Register Color Ball Sort Puzzle.
Layout disesuaikan lebih dekat ke desain Figma:
- LOGIN   : satu card putih di tengah window (centered).
- REGISTER: split 2 kolom - kiri logo besar + tagline, kanan form card.

Window fixed 1440x1024, konsisten dengan screen lain (lihat theme.py).
Login & Register benar-benar terhubung ke database lewat
database/queries.py (queries.login_user, queries.register_user).
"""

import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from database import queries
from theme import LEBAR_WINDOW, TINGGI_WINDOW, BG_COLOR, PRIMARY_BLUE, TEXT_DARK, TEXT_MUTED

CARD_COLOR = "#FFFFFF"
INPUT_BG = "#EDEFFB"
BORDER_MUTED = "#D8DCF5"


class LoginScreen(tk.Frame):
    def __init__(self, parent, on_login_success=None):
        """
        :param parent: widget induk (container di main.py)
        :param on_login_success: callback(user_data: dict) dipanggil setelah
                                  login berhasil.
        """
        super().__init__(parent, bg=BG_COLOR, width=LEBAR_WINDOW, height=TINGGI_WINDOW)
        self.pack_propagate(False)

        self.on_login_success = on_login_success

        self._muat_logo()

        self.login_frame = tk.Frame(self, bg=BG_COLOR, width=LEBAR_WINDOW, height=TINGGI_WINDOW)
        self.register_frame = tk.Frame(self, bg=BG_COLOR, width=LEBAR_WINDOW, height=TINGGI_WINDOW)
        self.login_frame.pack_propagate(False)
        self.register_frame.pack_propagate(False)

        self._bangun_login_frame()
        self._bangun_register_frame()

        self.show_login()

    # ------------------------------------------------------------
    # ASET GAMBAR
    # ------------------------------------------------------------
    def _muat_logo(self):
        """Memuat logo dari folder 'aset' di root project (opsional)."""
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            logo_path = os.path.join(base_dir, "aset", "logo_baru.PNG")
            logo_image = Image.open(logo_path).resize((110, 110))
            self.logo_photo = ImageTk.PhotoImage(logo_image)
        except Exception as e:
            print(f"[WARNING] Gagal memuat logo dari folder 'aset': {e}")
            self.logo_photo = None

    def _gambar_ikon_logo(self, parent, ukuran=110):
        """
        Menggambar ikon logo (kotak biru rounded + 3 tabung putih) memakai
        Canvas, sesuai desain Figma - dipakai kalau file logo_baru.PNG
        tidak ada / gagal dimuat, supaya UI tetap konsisten.
        """
        if self.logo_photo is not None:
            label = tk.Label(parent, image=self.logo_photo, bg=parent["bg"])
            label.image = self.logo_photo
            return label

        canvas = tk.Canvas(parent, width=ukuran, height=ukuran, bg=parent["bg"], highlightthickness=0)
        canvas.create_rectangle(4, 4, ukuran - 4, ukuran - 4, fill=PRIMARY_BLUE, outline="")

        lebar_tabung = 14
        jarak = 22
        x_awal = ukuran / 2 - jarak
        y0, y1 = ukuran * 0.28, ukuran * 0.72
        warna_bola = ["#EF4444", "#3B82F6", "#F59E0B"]

        for i in range(3):
            x = x_awal + i * jarak
            canvas.create_rectangle(x - lebar_tabung / 2, y0, x + lebar_tabung / 2, y1,
                                     outline="white", width=2)
            canvas.create_oval(x - 4, y1 - 14, x + 4, y1 - 6, fill=warna_bola[i], outline="")

        return canvas

    # ------------------------------------------------------------
    # NAVIGASI ANTAR FRAME (LOGIN <-> REGISTER)
    # ------------------------------------------------------------
    def show_login(self):
        self.register_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)

    def show_register(self):
        self.login_frame.pack_forget()
        self.register_frame.pack(fill="both", expand=True)

    # ==============================================================
    # LOGIN - card tunggal di tengah window
    # ==============================================================
    def _bangun_login_frame(self):
        f = self.login_frame

        card = tk.Frame(f, bg=CARD_COLOR, width=460, highlightbackground="#E5E7EB", highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center")

        isi = tk.Frame(card, bg=CARD_COLOR)
        isi.pack(padx=44, pady=40)

        self._gambar_ikon_logo(isi, ukuran=90).pack(pady=(0, 16))

        tk.Label(
            isi, text="Color Sort Ball", font=("Arial", 20, "bold"),
            bg=CARD_COLOR, fg=PRIMARY_BLUE,
        ).pack(pady=(0, 24))

        # --- Nama Pengguna ---
        tk.Label(
            isi, text="Nama Pengguna", font=("Arial", 9, "bold"),
            bg=CARD_COLOR, fg=TEXT_DARK,
        ).pack(anchor="w")

        self.login_username = tk.Entry(
            isi, font=("Arial", 11), bg=INPUT_BG, relief="flat", width=32,
            highlightthickness=1, highlightbackground=BORDER_MUTED, highlightcolor=PRIMARY_BLUE,
        )
        self.login_username.pack(ipady=8, pady=(4, 16))

        # --- Kata Sandi ---
        tk.Label(
            isi, text="Kata Sandi", font=("Arial", 9, "bold"),
            bg=CARD_COLOR, fg=TEXT_DARK,
        ).pack(anchor="w")

        baris_password = tk.Frame(isi, bg=INPUT_BG, highlightthickness=1,
                                   highlightbackground=BORDER_MUTED)
        baris_password.pack(fill="x", pady=(4, 8))

        self.login_password = tk.Entry(
            baris_password, font=("Arial", 11), bg=INPUT_BG, relief="flat", show="*",
        )
        self.login_password.pack(side="left", fill="x", expand=True, ipady=8, padx=(8, 0))

        self.login_show = tk.BooleanVar()
        tk.Checkbutton(
            baris_password, text="\U0001F441", variable=self.login_show,
            command=self._toggle_login_password, bg=INPUT_BG, relief="flat",
            bd=0, highlightthickness=0,
        ).pack(side="right")

        # --- Tombol Masuk ---
        tk.Button(
            isi, text="Masuk  \u2192", font=("Arial", 11, "bold"), bg=PRIMARY_BLUE,
            fg="white", relief="flat", width=32, pady=10, command=self._login,
        ).pack(pady=(16, 10))

        # --- Tombol Daftar (outline) ---
        tk.Button(
            isi, text="Daftar", font=("Arial", 11, "bold"), bg=CARD_COLOR,
            fg=PRIMARY_BLUE, relief="solid", bd=1, width=32, pady=10,
            command=self.show_register,
        ).pack(pady=(0, 16))

        tk.Label(
            isi, text="Selamat datang kembali, mari urutkan bolanya!",
            font=("Arial", 9), bg=CARD_COLOR, fg=TEXT_MUTED,
        ).pack()

    def _toggle_login_password(self):
        self.login_password.config(show="" if self.login_show.get() else "*")

    def _login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "Username dan Password harus diisi!")
            return

        berhasil, hasil = queries.login_user(username, password)

        if not berhasil:
            messagebox.showerror("Login Gagal", hasil)
            return

        messagebox.showinfo("Login", f"Selamat datang, {hasil['username']}!")

        if self.on_login_success:
            self.on_login_success(hasil)

    # ==============================================================
    # REGISTER - split 2 kolom (kiri logo & tagline, kanan form card)
    # ==============================================================
    def _bangun_register_frame(self):
        f = self.register_frame

        # --- Kolom kiri: logo besar + tagline ---
        kolom_kiri = tk.Frame(f, bg=BG_COLOR)
        kolom_kiri.place(relx=0.28, rely=0.5, anchor="center")

        self._gambar_ikon_logo(kolom_kiri, ukuran=140).pack(pady=(0, 20))

        tk.Label(
            kolom_kiri, text="Color Sort Ball", font=("Arial", 24, "bold"),
            bg=BG_COLOR, fg=PRIMARY_BLUE,
        ).pack()

        tk.Label(
            kolom_kiri,
            text="Susun warna, asah logika, dan raih skor\ntertinggi dalam petualangan teka-teki\nyang menyenangkan!",
            font=("Arial", 10), bg=BG_COLOR, fg=TEXT_MUTED, justify="center",
        ).pack(pady=(12, 0))

        # --- Kolom kanan: card form register ---
        card = tk.Frame(f, bg=CARD_COLOR, width=460, highlightbackground="#E5E7EB", highlightthickness=1)
        card.place(relx=0.68, rely=0.5, anchor="center")

        isi = tk.Frame(card, bg=CARD_COLOR)
        isi.pack(padx=40, pady=36)

        tk.Label(
            isi, text="Buat Akun Baru", font=("Arial", 18, "bold"),
            bg=CARD_COLOR, fg=TEXT_DARK,
        ).pack()

        tk.Label(
            isi, text="Ayo bergabung dan mulai bermain sekarang!",
            font=("Arial", 9), bg=CARD_COLOR, fg=TEXT_MUTED,
        ).pack(pady=(2, 20))

        tk.Label(
            isi, text="Nama Pengguna", font=("Arial", 9, "bold"),
            bg=CARD_COLOR, fg=TEXT_DARK,
        ).pack(anchor="w")
        self.reg_username = tk.Entry(
            isi, font=("Arial", 11), bg=INPUT_BG, relief="flat", width=32,
            highlightthickness=1, highlightbackground=BORDER_MUTED, highlightcolor=PRIMARY_BLUE,
        )
        self.reg_username.pack(ipady=8, pady=(4, 14))

        tk.Label(
            isi, text="Kata Sandi", font=("Arial", 9, "bold"),
            bg=CARD_COLOR, fg=TEXT_DARK,
        ).pack(anchor="w")
        baris_pw = tk.Frame(isi, bg=INPUT_BG, highlightthickness=1, highlightbackground=BORDER_MUTED)
        baris_pw.pack(fill="x", pady=(4, 14))
        self.reg_password = tk.Entry(baris_pw, font=("Arial", 11), bg=INPUT_BG, relief="flat", show="*")
        self.reg_password.pack(side="left", fill="x", expand=True, ipady=8, padx=(8, 0))

        self.register_show = tk.BooleanVar()
        tk.Checkbutton(
            baris_pw, text="\U0001F441", variable=self.register_show,
            command=self._toggle_register_password, bg=INPUT_BG, relief="flat",
            bd=0, highlightthickness=0,
        ).pack(side="right")

        tk.Label(
            isi, text="Konfirmasi Kata Sandi", font=("Arial", 9, "bold"),
            bg=CARD_COLOR, fg=TEXT_DARK,
        ).pack(anchor="w")
        self.reg_confirm = tk.Entry(
            isi, font=("Arial", 11), bg=INPUT_BG, relief="flat", width=32, show="*",
            highlightthickness=1, highlightbackground=BORDER_MUTED, highlightcolor=PRIMARY_BLUE,
        )
        self.reg_confirm.pack(ipady=8, pady=(4, 20))

        tk.Button(
            isi, text="Daftar Sekarang", font=("Arial", 11, "bold"), bg=PRIMARY_BLUE,
            fg="white", relief="flat", width=32, pady=10, command=self._register,
        ).pack(pady=(0, 12))

        baris_link = tk.Frame(isi, bg=CARD_COLOR)
        baris_link.pack()
        tk.Label(baris_link, text="Sudah punya akun? ", font=("Arial", 9),
                 bg=CARD_COLOR, fg=TEXT_MUTED).pack(side="left")
        tk.Button(
            baris_link, text="Kembali ke Masuk \u2192", font=("Arial", 9, "bold"),
            bg=CARD_COLOR, fg=PRIMARY_BLUE, relief="flat", bd=0,
            command=self.show_login,
        ).pack(side="left")

    def _toggle_register_password(self):
        tampil = "" if self.register_show.get() else "*"
        self.reg_password.config(show=tampil)
        self.reg_confirm.config(show=tampil)

    def _register(self):
        username = self.reg_username.get().strip()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()

        if username == "" or password == "" or confirm == "":
            messagebox.showerror("Error", "Semua data harus diisi!")
            return

        if password != confirm:
            messagebox.showerror("Error", "Konfirmasi password tidak cocok!")
            return

        berhasil, pesan = queries.register_user(username, password)

        if not berhasil:
            messagebox.showerror("Registrasi Gagal", pesan)
            return

        messagebox.showinfo("Registrasi", pesan)

        self.reg_username.delete(0, tk.END)
        self.reg_password.delete(0, tk.END)
        self.reg_confirm.delete(0, tk.END)
        self.show_login()
