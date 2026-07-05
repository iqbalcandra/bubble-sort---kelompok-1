import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Pilih Tingkat Kesulitan")
root.geometry("900x500")
root.resizable(False, False)
root.configure(bg="#f5f5f5")


def pilih(level):
    messagebox.showinfo(
        "Level Dipilih",
        f"Anda memilih tingkat kesulitan {level}"
    )


def kembali():
    root.destroy()

# Judul


tk.Label(
    root,
    text="Pilih Tingkat Kesulitan",
    font=("Arial", 22, "bold"),
    bg="#f5f5f5"
).pack(pady=(30, 5))

tk.Label(
    root,
    text="Tentukan tantanganmu hari ini dan mulailah bermain!",
    font=("Arial", 11),
    bg="#f5f5f5",
    fg="gray40"
).pack()


# Card


card_frame = tk.Frame(root, bg="#f5f5f5")
card_frame.pack(pady=40)


def buat_card(parent, tingkat, judul, deskripsi, warna):
    # yg di dalam kurung itu parameter, parent itu tempat card akan ditempatkan, tingkat itu level kesulitan, judul itu nama level,
    # deskripsi itu penjelasan level, dan warna itu warna tombol pilih.

    card = tk.Frame(
        parent,
        bg="white",
        width=220,
        height=260,
        relief="solid",
        bd=1
    )

    card.pack(side="left", padx=15)
    card.pack_propagate(False)

    tk.Label(
        card,
        text=tingkat,
        bg="white",
        fg="gray",
        font=("Arial", 10, "bold")
    ).pack(pady=(20, 5))

    tk.Label(
        card,
        text=judul,
        bg="white",
        font=("Arial", 18, "bold")
    ).pack()

    tk.Label(
        card,
        text=deskripsi,
        bg="white",
        justify="center",
        wraplength=180
    ).pack(pady=20)

    tk.Button(
        card,
        text=f"Pilih {judul}",
        bg=warna,
        fg="white",
        width=18,
        command=lambda: pilih(judul)
    ).pack(side="bottom", pady=20)


buat_card(
    card_frame,
    "TINGKAT 1",
    "Mudah",
    "Cocok untuk memulai\npetualangan pertamamu.\n\nSantai dan menyenangkan!",
    "#4CAF50"
)

buat_card(
    card_frame,
    "TINGKAT 2",
    "Sedang",
    "Butuh sedikit konsentrasi\nlebih untuk memilah semua\nbola berwarna.",
    "#FFC107"
)

buat_card(
    card_frame,
    "TINGKAT 3",
    "Sulit",
    "Hanya untuk para ahli!\n\nBanyak bola dan tabung\nyang menantang otak.",
    "#F44336"
)

# Tombol kembali

tk.Button(
    root,
    text="Kembali",
    width=15,
    command=kembali
).pack(pady=15)

root.mainloop()
