import os
import tkinter as tk
from PIL import Image, ImageTk


# ---------------------------------------------
# FUNGSI
# ---------------------------------------------

def coba_lagi():
    print("Coba Lagi")


def kembali_menu():
    print("Kembali ke Menu")


# ---------------------------------------------
# WINDOW
# ---------------------------------------------

root = tk.Tk()
root.title("Permainan Berakhir")

root.geometry("1440x1024")   
root.state("zoomed")          
root.minsize(1440, 1024)

root.configure(bg="#FDECEC")


# ---------------------------------------------
# PATH ASET
# ---------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

folder = os.path.join(
    BASE_DIR,
    "aset",
    "Icon permainan berakhir"
)


# ---------------------------------------------
# LOAD GAMBAR
# ---------------------------------------------

gambar_over = Image.open(
    os.path.join(folder, "Gambar berakhir.png")
)
gambar_over = gambar_over.resize((85,85))
gambar_over = ImageTk.PhotoImage(gambar_over)


icon_retry = Image.open(
    os.path.join(folder, "Icon coba lagi.png")
)
icon_retry = icon_retry.resize((18,18))
icon_retry = ImageTk.PhotoImage(icon_retry)


icon_home = Image.open(
    os.path.join(folder, "Icon home.png")
)
icon_home = icon_home.resize((18,18))
icon_home = ImageTk.PhotoImage(icon_home)


icon_waktu = Image.open(
    os.path.join(folder, "Icon waktu habis.png")
)
icon_waktu = icon_waktu.resize((15,15))
icon_waktu = ImageTk.PhotoImage(icon_waktu)


# ---------------------------------------------
# CARD
# ---------------------------------------------

card = tk.Frame(
    root,
    bg="white",
    bd=1,
    relief="solid",
    width=560,
    height=460
)

card.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)

card.pack_propagate(False)


tk.Label(
    card,
    image=gambar_over,
    bg="white"
).pack(pady=(30,12))


tk.Label(
    card,
    text="Permainan Berakhir!",
    font=("Arial",28,"bold"),
    bg="white",
    fg="#222222"
).pack()


badge = tk.Frame(
    card,
    bg="#FFE2E2"
)

badge.pack(
    pady=20,
    ipadx=5
)


tk.Label(
    badge,
    image=icon_waktu,
    bg="#FFE2E2"
).pack(
    side="left",
    padx=(8,4)
)


tk.Label(
    badge,
    text="Waktu Habis! Anda gagal menyelesaikan level Medium.",
    font=("Arial",9),
    bg="#FFE2E2",
    fg="#D32F2F"
).pack(
    side="left",
    padx=(0,8),
    pady=5
)

# ---------------------------------------------
# TOMBOL
# ---------------------------------------------

tk.Button(
    card,
    image=icon_retry,
    compound="left",
    text="  Coba Lagi",
    font=("Arial", 11, "bold"),
    bg="#1565D8",
    fg="white",
    activebackground="#1565D8",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=coba_lagi
).pack(
    fill="x",
    padx=55,
    pady=(10, 12),
    ipady=10
)


tk.Button(
    card,
    image=icon_home,
    compound="left",
    text="  Kembali ke Menu",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#1565D8",
    activebackground="white",
    activeforeground="#1565D8",
    relief="solid",
    bd=1,
    cursor="hand2",
    command=kembali_menu
).pack(
    fill="x",
    padx=55,
    ipady=10
)


# ---------------------------------------------
# MENJALANKAN PROGRAM
# ---------------------------------------------

root.mainloop()