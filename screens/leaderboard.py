import tkinter as tk
# import menuscreen


def kembali():
    root.destroy()

    # menu_root = tk.Tk()
    # menuscreen.MenuScreen(menu_root)
    # menu_root.mainloop()


root = tk.Tk()
root.title("Leaderboard")
root.geometry("850x550")
root.resizable(False, False)
root.configure(bg="#f3f4f6")

# ===========================
# Judul
# ===========================

tk.Label(
    root,
    text="Leaderboard",
    font=("Arial", 20, "bold"),
    bg="#f3f4f6",
    fg="#0f5bb5"
).pack(anchor="w", padx=30, pady=15)

# ===========================
# Card Putih
# ===========================

card = tk.Frame(root, bg="white", bd=1, relief="solid")
card.pack(padx=60, pady=10, fill="both", expand=True)

# ===========================
# Header Abu
# ===========================

header = tk.Frame(card, bg="#0056C6", height=45)
header.pack(fill="x")

tk.Label(
    header,
    text=" Top 5 Pemain Terbaik ",
    bg="#0056C6",
    fg="white",
    font=("Arial", 12, "bold")
).pack(side="left", padx=20, pady=10)


# ===========================
# Judul Kolom
# ===========================

judul = tk.Frame(card, bg="white")
judul.pack(fill="x", padx=20, pady=10)

judul_data = [
    ("Peringkat", 12),
    ("Nama", 28),
    ("Skor", 12),
    ("Level", 12),
    ("Tanggal", 15)
]

for text, width in judul_data:
    tk.Label(
        judul,
        text=text,
        width=width,
        bg="white",
        fg="gray30",
        font=("Arial", 9, "bold")
    ).pack(side="left")

# ===========================
# Data Dummy
# ===========================

data = [
    ("1", "Andi Pratama", "12,450", "Level 24", "12 Okt 2023"),
    ("2", "Siti Rahayu", "11,200", "Level 21", "11 Okt 2023"),
    ("3", "Budi Santoso", "10,850", "Level 19", "12 Okt 2023"),
    ("4", "Lani Wijaya", "9,400", "Level 17", "10 Okt 2023"),
    ("5", "Anda", "8,900", "Level 12", "Hari Ini")
]

# ===========================
# Isi Leaderboard
# ===========================

for pemain in data:

    row = tk.Frame(card, bg="white")
    row.pack(fill="x", padx=20, pady=6)

    tk.Label(row, text=pemain[0], width=12,
             bg="white").pack(side="left")

    tk.Label(row, text=pemain[1], width=28,
             anchor="w", bg="white").pack(side="left")

    tk.Label(row, text=pemain[2], width=12,
             bg="white", font=("Arial", 10, "bold")).pack(side="left")

    tk.Label(
        row,
        text=pemain[3],
        width=12,
        bg="#dddddd"
    ).pack(side="left")

    tk.Label(row, text=pemain[4], width=15,
             bg="white").pack(side="left")

# berfungsi untuk mengambil setiap data pemain satu per satu dari list data, kemudian membuat satu baris leaderboard untuk setiap pemain.

# ===========================
# Footer
# ===========================

footer = tk.Frame(card, bg="white")
footer.pack(fill="x", side="bottom", pady=15, padx=20)


tk.Button(
    footer,
    text=" <- Kembali",
    width=15,
    bg="#0056C6",
    fg="white",
    command=kembali
).pack(side="right")

root.mainloop()
