import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

root = tk.Tk()
root.title("Color Ball Sort Puzzle")
root.geometry("450x450")
root.resizable(False, False)


# Fungsi


def show_login():
    register_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)


def show_register():
    login_frame.pack_forget()
    register_frame.pack(fill="both", expand=True)


def login():
    username = login_username.get()
    password = login_password.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "Username dan Password harus diisi!")
        return

    messagebox.showinfo("Login", f"Selamat datang, {username}!")


def register():
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


def show_login_password():
    if login_show.get():
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

# logo


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
logo_path = os.path.join(BASE_DIR, "aset", "logo_bubble.jpeg")

logo_image = Image.open(logo_path)
logo_image = logo_image.resize((120, 120))

login_frame = tk.Frame(root)

logo = ImageTk.PhotoImage(logo_image)

tk.Label(login_frame, image=logo).pack(pady=10)


# tampilan

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


register_frame = tk.Frame(root)

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


show_login()

root.mainloop()
