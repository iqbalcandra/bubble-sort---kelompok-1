import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import sys

# ===============================
# WINDOW
# ===============================

root = tk.Tk()
root.title("Color Ball Sort Puzzle")
root.geometry("1100x650")
root.state("zoomed")
root.configure(bg="#F5F5F5")
root.resizable(False, False)

# ===============================
# LOAD GAMBAR
# ===============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logo_path = os.path.join(BASE_DIR, "aset", "logo_baru.PNG")

logo_img = Image.open(logo_path)
logo_img = logo_img.resize((120, 120))

logo = ImageTk.PhotoImage(logo_img)

# ===============================
# FUNGSI
# ===============================


def login():

    username = login_username.get()
    password = login_password.get()

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
    root.destroy()

    # Jalankan menu screen
    menu_path = os.path.join(BASE_DIR, "screens", "menu_screen.py")

    subprocess.Popen([sys.executable, menu_path])


def register():

    if reg_username.get() == "" \
            or reg_password.get() == "" \
            or reg_confirm.get() == "":

        messagebox.showerror(
            "Error",
            "Semua data harus diisi!"
        )
        return

    if reg_password.get() != reg_confirm.get():

        messagebox.showerror(
            "Error",
            "Konfirmasi password tidak cocok!"
        )
        return

    messagebox.showinfo(
        "Berhasil",
        "Registrasi berhasil.\nSilakan login."
    )

    show_login()


def show_login():
    login_card.pack(expand=True)
    register_card.pack_forget()


def show_register():
    register_card.pack(expand=True)
    login_card.pack_forget()


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

# ===============================
# MAIN FRAME
# ===============================


main = tk.Frame(
    root,
    bg="#F5F5F5"
)

main.pack(
    fill="both",
    expand=True,
    padx=40,
    pady=30
)

# ===============================
# BAGIAN KIRI
# ===============================

left = tk.Frame(
    main,
    bg="#F5F5F5"
)

left.pack(
    side="left",
    fill="both",
    expand=True
)

tk.Label(
    left,
    image=logo,
    bg="#F5F5F5"
).pack(
    pady=(120, 20)
)

tk.Label(
    left,
    text="Color Ball Sort Puzzle",
    font=("Arial", 24, "bold"),
    fg="#1565D8",
    bg="#F5F5F5"
).pack()

tk.Label(
    left,
    text="Susun warna, asah logika,\ndan raih skor tertinggi\nbersama teman-temanmu!",
    font=("Arial", 11),
    fg="gray",
    bg="#F5F5F5",
    justify="center"
).pack(
    pady=15
)

# ===============================
# BAGIAN KANAN
# ===============================

right = tk.Frame(
    main,
    bg="#F5F5F5"
)

right.pack(
    side="right",
    fill="both",
    expand=True
)

# ===============================
# LOGIN CARD
# ===============================

login_card = tk.Frame(
    right,
    bg="white",
    width=360,
    height=550,
    bd=1,
    relief="solid"
)

login_card.pack_propagate(False)
login_card.pack(expand=True)

tk.Label(
    login_card,
    image=logo,
    bg="white"
).pack(pady=(25, 10))

tk.Label(
    login_card,
    text="Color Ball Sort Puzzle",
    font=("Arial", 16, "bold"),
    fg="#1565D8",
    bg="white"
).pack()

tk.Label(
    login_card,
    text="Selamat Datang Kembali",
    font=("Arial", 10),
    bg="white",
    fg="gray"
).pack(pady=(0, 20))

# ---------------- Username ----------------

tk.Label(
    login_card,
    text="Username",
    bg="white",
    font=("Arial", 10, "bold")
).pack(anchor="w", padx=35)

login_username = tk.Entry(
    login_card,
    width=35,
    font=("Arial", 11)
)

login_username.pack(
    padx=35,
    pady=(5, 15),
    ipady=5
)

# ---------------- Password ----------------

tk.Label(
    login_card,
    text="Password",
    bg="white",
    font=("Arial", 10, "bold")
).pack(anchor="w", padx=35)

login_password = tk.Entry(
    login_card,
    width=35,
    font=("Arial", 11),
    show="*"
)

login_password.pack(
    padx=35,
    pady=(5, 5),
    ipady=5
)

login_show = tk.BooleanVar()

tk.Checkbutton(
    login_card,
    text="Tampilkan Password",
    variable=login_show,
    command=show_login_password,
    bg="white"
).pack(
    anchor="w",
    padx=35,
    pady=(0, 20)
)

# ---------------- Tombol Login ----------------

tk.Button(
    login_card,
    text="Masuk",
    bg="#1565D8",
    fg="white",
    font=("Arial", 11, "bold"),
    width=28,
    height=2,
    relief="flat",
    cursor="hand2",
    command=login
).pack()

# ---------------- Pindah Register ----------------

frame_bawah = tk.Frame(
    login_card,
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
    command=show_register
).pack(side="left")

# ===============================
# REGISTER CARD
# ===============================

register_card = tk.Frame(
    right,
    bg="white",
    width=360,
    height=550,
    bd=1,
    relief="solid"
)

register_card.pack_propagate(False)
register_card.pack(expand=True)
register_card.pack_forget()

tk.Label(
    register_card,
    image=logo,
    bg="white"
).pack(pady=(20, 10))

tk.Label(
    register_card,
    text="Buat Akun Baru",
    font=("Arial", 16, "bold"),
    fg="#1565D8",
    bg="white"
).pack()

tk.Label(
    register_card,
    text="Daftar dan mulai petualanganmu!",
    font=("Arial", 10),
    bg="white",
    fg="gray"
).pack(pady=(0, 20))

# ---------- Username ----------

tk.Label(
    register_card,
    text="Username",
    bg="white",
    font=("Arial", 10, "bold")
).pack(anchor="w", padx=35)

reg_username = tk.Entry(
    register_card,
    width=35,
    font=("Arial", 11)
)

reg_username.pack(
    padx=35,
    pady=(5, 15),
    ipady=5
)

# ---------- Password ----------

tk.Label(
    register_card,
    text="Password",
    bg="white",
    font=("Arial", 10, "bold")
).pack(anchor="w", padx=35)

reg_password = tk.Entry(
    register_card,
    width=35,
    font=("Arial", 11),
    show="*"
)

reg_password.pack(
    padx=35,
    pady=(5, 15),
    ipady=5
)

# ---------- Konfirmasi Password ----------

tk.Label(
    register_card,
    text="Konfirmasi Password",
    bg="white",
    font=("Arial", 10, "bold")
).pack(anchor="w", padx=35)

reg_confirm = tk.Entry(
    register_card,
    width=35,
    font=("Arial", 11),
    show="*"
)

reg_confirm.pack(
    padx=35,
    pady=(5, 5),
    ipady=5
)

# ---------- Show Password ----------

register_show = tk.BooleanVar()

tk.Checkbutton(
    register_card,
    text="Tampilkan Password",
    variable=register_show,
    command=show_register_password,
    bg="white"
).pack(
    anchor="w",
    padx=35,
    pady=(0, 20)
)

# ---------- Tombol Register ----------

tk.Button(
    register_card,
    text="Daftar",
    bg="#1565D8",
    fg="white",
    font=("Arial", 11, "bold"),
    width=28,
    height=2,
    relief="flat",
    cursor="hand2",
    command=register
).pack()

# ---------- Kembali Login ----------

frame_login = tk.Frame(
    register_card,
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
    command=show_login
).pack(side="left")


login_card.pack(expand=True)
register_card.pack_forget()

root.mainloop()
