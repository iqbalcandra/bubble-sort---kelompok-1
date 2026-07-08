# modul untuk urusan path/file sistem operasi
import os
# untuk menjalankan file python lain sebagai proses baru
import subprocess
# untuk ambil path interpreter python yang sedang jalan
import sys
import tkinter as tk                        # library utama untuk bikin GUI
# untuk munculin popup pesan (error/info)
from tkinter import messagebox

# Pillow: untuk buka & convert gambar ke format tkinter
from PIL import Image, ImageTk


# class utama halaman Login & Register
class LoginScreen(tk.Frame):

    # constructor, dijalankan otomatis saat LoginScreen() dibuat
    def __init__(self):

        # ===============================
        # WINDOW
        # ===============================

        self.root = tk.Tk()                             # bikin window utama tkinter
        # judul window (muncul di title bar)
        self.root.title("Color Ball Sort Puzzle")
        # ukuran default window (lebar x tinggi)
        self.root.geometry("1100x650")
        # window dibuka dalam kondisi maximize
        self.root.state("zoomed")
        # warna background window
        self.root.configure(bg="#F5F5F5")
        # window tidak bisa di-resize (lebar & tinggi dikunci)
        self.root.resizable(False, False)

        # ===============================
        # PATH
        # ===============================

        self.BASE_DIR = os.path.dirname(                # ambil folder tempat file ini berada,
            # lalu naik satu folder lagi -> jadi root project
            os.path.dirname(os.path.abspath(__file__)))

        # ===============================
        # LOAD GAMBAR
        # ===============================

        # susun path lengkap ke file logo
        logo_path = os.path.join(self.BASE_DIR, "aset", "logo_baru.PNG")

        # buka file gambar logo pakai Pillow
        logo_img = Image.open(logo_path)
        # ubah ukuran logo jadi 120x120 pixel
        logo_img = logo_img.resize((120, 120))

        # convert gambar Pillow ke format yang bisa dipakai tkinter
        self.logo = ImageTk.PhotoImage(logo_img)

        # ===============================
        # BUILD UI
        # ===============================

        self._build_main_frame()        # bangun frame utama pembungkus seluruh halaman
        self._build_left_section()      # bangun bagian kiri (logo + judul + deskripsi game)
        # bangun bagian kanan (wadah kosong untuk card login/register)
        self._build_right_section()
        self._build_login_card()        # bangun card form Login
        self._build_register_card()     # bangun card form Register

        # tampilkan card Login saat pertama kali dibuka
        self.login_card.pack(expand=True)
        # sembunyikan card Register (belum ditampilkan)
        self.register_card.pack_forget()

    # ===============================
    # FUNGSI
    # ===============================

    def login(self):                                    # dipanggil saat tombol "Masuk" diklik

        # ambil teks yang diketik di input Username
        username = self.login_username.get()
        # ambil teks yang diketik di input Password
        password = self.login_password.get()

        if username == "" or password == "":            # kalau salah satu kosong
            messagebox.showerror(                        # tampilkan popup error
                "Error",
                "Username dan Password harus diisi!"
            )
            return                                        # hentikan fungsi, tidak lanjut login

        messagebox.showinfo(                             # tampilkan popup sukses/selamat datang
            "Login",
            f"Selamat datang, {username}"
        )

        # Tutup window login
        # tutup/hancurkan window login sekarang
        self.root.destroy()

        # Jalankan menu screen
        # susun path ke file menu_screen.py
        menu_path = os.path.join(self.BASE_DIR, "screens", "menu_screen.py")

        # jalankan menu_screen.py sebagai proses/program baru
        subprocess.Popen([sys.executable, menu_path])

    def register(self):                                  # dipanggil saat tombol "Daftar" diklik

        if self.reg_username.get() == "" \
                or self.reg_password.get() == "" \
                or self.reg_confirm.get() == "":          # kalau ada salah satu field register yang kosong

            messagebox.showerror(                        # tampilkan popup error
                "Error",
                "Semua data harus diisi!"
            )
            return                                        # hentikan fungsi

        if self.reg_password.get() != self.reg_confirm.get():   # kalau password & konfirmasi tidak sama

            messagebox.showerror(                        # tampilkan popup error
                "Error",
                "Konfirmasi password tidak cocok!"
            )
            return                                        # hentikan fungsi

        messagebox.showinfo(                             # kalau semua valid, tampilkan popup berhasil
            "Berhasil",
            "Registrasi berhasil.\nSilakan login."
        )

        # otomatis pindah tampilan ke card Login
        self.show_login()

    # fungsi untuk menampilkan card Login
    def show_login(self):
        self.login_card.pack(expand=True)                # tampilkan card Login
        self.register_card.pack_forget()                 # sembunyikan card Register

    # fungsi untuk menampilkan card Register
    def show_register(self):
        # tampilkan card Register
        self.register_card.pack(expand=True)
        self.login_card.pack_forget()                     # sembunyikan card Login

    # toggle lihat/sembunyikan password di form Login
    def show_login_password(self):

        if self.login_show.get():                         # kalau checkbox "Tampilkan Password" dicentang
            # tampilkan password apa adanya (tidak disensor)
            self.login_password.config(show="")
        else:
            # sensor password jadi tanda bintang
            self.login_password.config(show="*")

    # toggle lihat/sembunyikan password di form Register
    def show_register_password(self):

        if self.register_show.get():                      # kalau checkbox "Tampilkan Password" dicentang

            # tampilkan password asli
            self.reg_password.config(show="")
            # tampilkan konfirmasi password asli
            self.reg_confirm.config(show="")

        else:

            # sensor password jadi bintang
            self.reg_password.config(show="*")
            # sensor konfirmasi password jadi bintang
            self.reg_confirm.config(show="*")

    # ===============================
    # BUILD UI - HELPER
    # ===============================

    # bikin frame pembungkus utama (kiri + kanan)
    def _build_main_frame(self):

        self.main = tk.Frame(
            self.root,
            bg="#F5F5F5"                                  # warna background sama dengan window
        )

        self.main.pack(
            fill="both",                                  # frame memenuhi lebar & tinggi window
            expand=True,                                  # ikut membesar kalau window di-resize
            # jarak kosong kiri-kanan dari tepi window
            padx=40,
            # jarak kosong atas-bawah dari tepi window
            pady=30
        )

    # bikin bagian kiri: logo, judul, deskripsi
    def _build_left_section(self):

        self.left = tk.Frame(
            self.main,
            bg="#F5F5F5"
        )

        self.left.pack(
            side="left",                                  # ditempatkan di sisi kiri
            fill="both",                                   # mengisi ruang yang tersedia
            expand=True                                    # ikut membesar/mengecil sesuai window
        )

        tk.Label(
            self.left,
            image=self.logo,                               # tampilkan gambar logo
            bg="#F5F5F5"
        ).pack(
            # jarak atas 120px, bawah 20px
            pady=(120, 20)
        )

        tk.Label(
            self.left,
            text="Color Ball Sort Puzzle",                  # judul game
            font=("Arial", 24, "bold"),
            fg="#1565D8",                                    # warna teks biru
            bg="#F5F5F5"
        ).pack()

        tk.Label(
            self.left,
            # tagline/deskripsi game
            text="Susun warna, asah logika,\ndan raih skor tertinggi\nbersama teman-temanmu!",
            font=("Arial", 11),
            fg="gray",
            bg="#F5F5F5",
            justify="center"                                 # teks multi-baris rata tengah
        ).pack(
            pady=15
        )

    # bikin bagian kanan: wadah kosong utk card
    def _build_right_section(self):

        self.right = tk.Frame(
            self.main,
            bg="#F5F5F5"
        )

        self.right.pack(
            side="right",                                    # ditempatkan di sisi kanan
            fill="both",
            expand=True
        )

    # bikin card/kotak putih berisi form Login
    def _build_login_card(self):

        self.login_card = tk.Frame(
            self.right,
            bg="white",
            width=360,                                       # lebar card tetap 360px
            height=550,                                       # tinggi card tetap 550px
            bd=1,                                             # ketebalan border 1px
            relief="solid"                                    # gaya border garis solid
        )

        # kunci ukuran card, tidak menyesuaikan isi
        self.login_card.pack_propagate(False)
        # tampilkan card di tengah section kanan
        self.login_card.pack(expand=True)

        tk.Label(
            self.login_card,
            image=self.logo,                                  # logo kecil di atas form
            bg="white"
        ).pack(pady=(25, 10))

        tk.Label(
            self.login_card,
            text="Color Ball Sort Puzzle",                     # nama game di dalam card
            font=("Arial", 16, "bold"),
            fg="#1565D8",
            bg="white"
        ).pack()

        tk.Label(
            self.login_card,
            text="Selamat Datang Kembali",                     # sub-judul/sapaan
            font=("Arial", 10),
            bg="white",
            fg="gray"
        ).pack(pady=(0, 20))

        # ---------------- Username ----------------

        tk.Label(
            self.login_card,
            text="Username",                                   # label untuk input username
            bg="white",
            font=("Arial", 10, "bold")
            # rata kiri, jarak kiri 35px
        ).pack(anchor="w", padx=35)

        self.login_username = tk.Entry(                        # input teks untuk username
            self.login_card,
            width=35,
            font=("Arial", 11)
        )

        self.login_username.pack(
            padx=35,
            pady=(5, 15),
            # tambah tinggi dalam input (padding vertikal)
            ipady=5
        )

        # ---------------- Password ----------------

        tk.Label(
            self.login_card,
            text="Password",                                    # label untuk input password
            bg="white",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", padx=35)

        self.login_password = tk.Entry(                        # input password
            self.login_card,
            width=35,
            font=("Arial", 11),
            show="*"                                            # karakter disensor jadi bintang
        )

        self.login_password.pack(
            padx=35,
            pady=(5, 5),
            ipady=5
        )

        # variabel status checkbox (dicentang/tidak)
        self.login_show = tk.BooleanVar()

        tk.Checkbutton(
            self.login_card,
            text="Tampilkan Password",                          # teks di sebelah checkbox
            # dihubungkan ke variabel status di atas
            variable=self.login_show,
            # fungsi yang dipanggil saat dicentang/dilepas
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
            text="Masuk",                                        # teks tombol
            bg="#1565D8",                                        # warna latar biru
            fg="white",                                          # warna teks putih
            font=("Arial", 11, "bold"),
            width=28,
            height=2,
            relief="flat",                                       # tombol tanpa border timbul
            # kursor jadi ikon tangan saat hover
            cursor="hand2",
            # fungsi yang dijalankan saat diklik
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
            text="Belum punya akun?",                            # teks ajakan daftar
            bg="white",
            fg="gray"
        ).pack(side="left")

        tk.Button(
            frame_bawah,
            # tombol pindah ke form Register
            text="Daftar",
            bg="white",
            fg="#1565D8",
            relief="flat",
            cursor="hand2",
            # panggil fungsi pindah tampilan ke Register
            command=self.show_register
        ).pack(side="left")

    # bikin card/kotak putih berisi form Register
    def _build_register_card(self):

        self.register_card = tk.Frame(
            self.right,
            bg="white",
            width=360,
            height=550,
            bd=1,
            relief="solid"
        )

        self.register_card.pack_propagate(
            False)                 # kunci ukuran card
        # pack dulu (nanti langsung disembunyikan lagi)
        self.register_card.pack(expand=True)
        # sembunyikan card Register di awal
        self.register_card.pack_forget()

        tk.Label(
            self.register_card,
            image=self.logo,                                      # logo di atas form register
            bg="white"
        ).pack(pady=(20, 10))

        tk.Label(
            self.register_card,
            text="Buat Akun Baru",                                 # judul form register
            font=("Arial", 16, "bold"),
            fg="#1565D8",
            bg="white"
        ).pack()

        tk.Label(
            self.register_card,
            text="Daftar dan mulai petualanganmu!",                 # sub-judul/ajakan
            font=("Arial", 10),
            bg="white",
            fg="gray"
        ).pack(pady=(0, 20))

        # ---------- Username ----------

        tk.Label(
            self.register_card,
            text="Username",                                       # label input username
            bg="white",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", padx=35)

        self.reg_username = tk.Entry(                             # input username untuk register
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
            text="Password",                                       # label input password
            bg="white",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", padx=35)

        self.reg_password = tk.Entry(                              # input password untuk register
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
            # label input konfirmasi password
            text="Konfirmasi Password",
            bg="white",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", padx=35)

        self.reg_confirm = tk.Entry(                               # input konfirmasi password
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

        # variabel status checkbox show password
        self.register_show = tk.BooleanVar()

        tk.Checkbutton(
            self.register_card,
            text="Tampilkan Password",
            variable=self.register_show,
            # fungsi toggle show/hide password
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
            text="Daftar",                                          # teks tombol daftar
            bg="#1565D8",
            fg="white",
            font=("Arial", 11, "bold"),
            width=28,
            height=2,
            relief="flat",
            cursor="hand2",
            # fungsi yang dijalankan saat diklik
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
            text="Sudah punya akun?",                                # teks ajakan login
            bg="white",
            fg="gray"
        ).pack(side="left")

        tk.Button(
            frame_login,
            # tombol pindah ke form Login
            text="Masuk",
            bg="white",
            fg="#1565D8",
            relief="flat",
            cursor="hand2",
            # panggil fungsi pindah tampilan ke Login
            command=self.show_login
        ).pack(side="left")

    # ===============================
    # RUN
    # ===============================

    # method untuk menjalankan window
    def run(self):
        # loop utama tkinter (menjaga window tetap terbuka)
        self.root.mainloop()


# hanya dijalankan kalau file ini dieksekusi langsung
if __name__ == "__main__":
    # buat objek LoginScreen
    app = LoginScreen()
    # jalankan window-nya
    app.run()
