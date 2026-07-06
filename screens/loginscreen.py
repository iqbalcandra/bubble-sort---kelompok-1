import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Color Ball Sort Puzzle")
root.geometry("450x550")
root.resizable(False, False)


# ==================== FUNGSI ====================

# Fungsi untuk menampilkan frame login
def show_login():
    # menyembunyikan frame register
    register_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)

# Fungsi untuk menampilkan frame register


def show_register():
    # menyembunyikan frame login
    login_frame.pack_forget()
    register_frame.pack(fill="both", expand=True)


def login():
    # mengambil isi username  dari entry login_username dan password dari entry login_password
    username = login_username.get()
    password = login_password.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "Username dan Password harus diisi!")
        return

    messagebox.showinfo("Login", f"Selamat datang, {username}!")


def register():
    # mengambil data dari entry register
    username = reg_username.get()
    password = reg_password.get()
    confirm = reg_confirm.get()

    if username == "" or password == "" or confirm == "":
        messagebox.showerror("Error", "Semua data harus diisi!")
        return

    if password != confirm:
        messagebox.showerror("Error", "Konfirmasi password tidak cocok!")
        return

    messagebox.showinfo(
        "Registrasi",
        "Akun berhasil dibuat.\nSilakan login."
    )

    show_login()

# untuk menampilakn / menyembukin password pada login dan register


def show_login_password():
    # jika checkbutton dicentang
    if login_show.get():
        # password akan munculs
        login_password.config(show="")
    else:
        login_password.config(show="*")


def show_register_password():
    if register_show.get():
        reg_password.config(show="")
        reg_confirm.config(show="")
    else:
        reg_password.config(show="*")
        reg_confirm.config(show="*")


# ==================== PROSES PEMBUATAN GAMBAR (MANDATORY DI SINI) ====================

# 1. Menentukan path folder aset (keluar 1 tingkat dari folder 'screens')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logo_path = os.path.join(BASE_DIR, "aset", "logo_baru.PNG")

# 2. Membuka file gambar asli menggunakan PIL
logo_image = Image.open(logo_path)
logo_image = logo_image.resize((120, 120))

# 3. Membuat objek PhotoImage untuk login dan register secara terpisah
logo_login = ImageTk.PhotoImage(logo_image)
logo_register = ImageTk.PhotoImage(logo_image)


# ==================== LOGIN SCREEN ====================

login_frame = tk.Frame(root)

# Menampilkan logo login (Variabel logo_login dijamin aman karena sudah dibuat di atas)
label_logo_login = tk.Label(login_frame, image=logo_login)
label_logo_login.image = logo_login
label_logo_login.pack(pady=10)

tk.Label(
    login_frame,
    text="COLOR BALL SORT PUZZLE",
    font=("Arial", 16, "bold")
).pack(pady=20)

tk.Label(login_frame, text="Username").pack()
login_username = tk.Entry(login_frame, width=30)
login_username.pack(pady=5)

tk.Label(login_frame, text="Password").pack()
login_password = tk.Entry(login_frame, width=30, show="*")
login_password.pack(pady=5)

login_show = tk.BooleanVar()
tk.Checkbutton(
    login_frame,
    text="Show Password",
    variable=login_show,
    command=show_login_password
).pack()

tk.Button(
    login_frame,
    text="Masuk",
    width=20,
    command=login
).pack(pady=10)

tk.Button(
    login_frame,
    text="Daftar",
    width=20,
    command=show_register
).pack()


# ==================== REGISTER SCREEN ====================

register_frame = tk.Frame(root)

# Menampilkan logo register
label_logo_reg = tk.Label(register_frame, image=logo_register)
label_logo_reg.image = logo_register
label_logo_reg.pack(pady=10)

tk.Label(
    register_frame,
    text="BUAT AKUN BARU",
    font=("Arial", 16, "bold")
).pack(pady=15)

tk.Label(register_frame, text="Username").pack()
reg_username = tk.Entry(register_frame, width=30)
reg_username.pack(pady=5)

tk.Label(register_frame, text="Password").pack()
reg_password = tk.Entry(register_frame, width=30, show="*")
reg_password.pack(pady=5)

tk.Label(register_frame, text="Konfirmasi Password").pack()
reg_confirm = tk.Entry(register_frame, width=30, show="*")
reg_confirm.pack(pady=5)

register_show = tk.BooleanVar()
tk.Checkbutton(
    register_frame,
    text="Show Password",
    variable=register_show,
    command=show_register_password
).pack()

tk.Button(
    register_frame,
    text="Daftar Sekarang",
    width=20,
    command=register
).pack(pady=10)

tk.Button(
    register_frame,
    text="Kembali ke Masuk",
    width=20,
    command=show_login
).pack()


# Menjalankan screen pertama kali
show_login()

root.mainloop()
