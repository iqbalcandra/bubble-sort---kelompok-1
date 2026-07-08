import tkinter as tk
from tkinter import ttk

# untuk menampilkan halaman level selesai setelah menyelesaikan level


def level_selesai(parent):
    # mengatur warna background halaman
    parent.configure(bg="#F5F7FB")

    frame = tk.Frame(parent, bg="#F5F7FB")
    frame.pack(expand=True, fill="both")

    # ================= ICON =================
    tk.Label(
        frame,
        text="⭐⭐⭐",
        font=("Arial", 18),
        bg="#F5F7FB",
        fg="#D97706"
    ).pack()

    tk.Label(
        frame,
        text="🏆",
        font=("Arial", 40),
        bg="#F5F7FB",
        fg="#D97706"
    ).pack()

    # ================= JUDUL =================
    tk.Label(
        frame,
        text="Level Selesai!",
        font=("Poppins", 22, "bold"),
        bg="#F5F7FB",
        fg="#1565D8"
    ).pack(pady=(10, 0))

    tk.Label(
        frame,
        text="Selamat! Kamu berhasil menyelesaikan level ini!",
        font=("Poppins", 9),
        bg="#F5F7FB",
        fg="gray"
    ).pack(pady=(0, 20))

    # ================= CARD =================
    # frame untuk menampilkan skor
    card = tk.Frame(
        frame,
        bg="white",
        bd=1,
        relief="solid"
    )
    card.pack()

    # Skor Dasar
    row1 = tk.Frame(card, bg="white")
    row1.pack(fill="x", padx=20, pady=10)

    tk.Label(
        row1,
        text="🎯 Skor Dasar",
        bg="white"
    ).pack(side="left")

    tk.Label(
        row1,
        text="200",
        bg="white",
        font=("Poppins", 10, "bold")
    ).pack(side="right")

    # Bonus
    row2 = tk.Frame(card, bg="white")
    row2.pack(fill="x", padx=20)

    tk.Label(
        row2,
        text="⏱ Bonus Waktu",
        bg="white"
    ).pack(side="left")

    tk.Label(
        row2,
        text="+450",
        bg="white",
        fg="#D97706",
        font=("Poppins", 10, "bold")
    ).pack(side="right")

    ttk.Separator(card).pack(fill="x", padx=20, pady=10)

    # Total
    total = tk.Frame(card, bg="#EAF2FF")
    total.pack(fill="x")

    tk.Label(
        total,
        text="TOTAL SKOR",
        bg="#EAF2FF",
        fg="#1565D8",
        font=("Poppins", 10, "bold")
    ).pack(pady=(8, 0))

    tk.Label(
        total,
        text="650",
        bg="#EAF2FF",
        fg="#1565D8",
        font=("Poppins", 24, "bold")
    ).pack(pady=(0, 10))

    # ================= BUTTON =================
    tk.Button(
        frame,
        text="Level Berikutnya →",
        bg="#1565D8",
        fg="white",
        width=28,
        height=2,
        relief="raised",
    ).pack(pady=20)

    bawah = tk.Frame(frame, bg="#F5F7FB")
    bawah.pack()

    tk.Button(
        bawah,
        text="↻ Ulangi",
        width=14
    ).pack(side="left", padx=5)

    tk.Button(
        bawah,
        text="☰ Menu Utama",
        width=14
    ).pack(side="left", padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Level Selesai")
    root.geometry("800x600")

    level_selesai(root)

    root.mainloop()
