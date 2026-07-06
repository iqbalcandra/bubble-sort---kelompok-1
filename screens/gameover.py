import tkinter as tk

# untuk menampilkan halaman game over


def tampil(parent):

    # menghapus widget yang ada pada halaman sebelumnya
    for widget in parent.winfo_children():
        widget.destroy()

    # untuk background halaman gameover
    parent.configure(bg="#FDECEC")

    # frame utama
    main = tk.Frame(parent, bg="#FDECEC")
    main.pack(expand=True)

    # ================= ICON =================
    tk.Label(
        main,
        text="☹",
        font=("Arial", 48),
        bg="#FDECEC",
        fg="#E53935"
    ).pack(pady=(20, 10))

    # ================= JUDUL =================
    tk.Label(
        main,
        text="Permainan Berakhir",
        font=("Poppins", 22, "bold"),
        bg="#FDECEC",
        fg="#E53935"
    ).pack()

    # pesan kepada pemain
    tk.Label(
        main,
        text="Waktu habis! Kamu belum berhasil\nmenyelesaikan level ini.",
        font=("Poppins", 10),
        bg="#FDECEC",
        fg="#555555",
        justify="center"
    ).pack(pady=(5, 20))

    # ================= CARD =================
    # frame untuk menampilkan pesan semangat
    card = tk.Frame(
        main,
        bg="white",
        bd=1,
        relief="solid",
        padx=25,
        pady=20
    )
    card.pack()

    tk.Label(
        card,
        text="💔",
        font=("Arial", 40),
        bg="white"
    ).pack()

    tk.Label(
        card,
        text="Jangan menyerah!",
        font=("Poppins", 14, "bold"),
        bg="white",
        fg="#E53935"
    ).pack(pady=(10, 5))

    tk.Label(
        card,
        text="Coba lagi dan raih skor terbaikmu!",
        font=("Poppins", 10),
        bg="white",
        fg="#666666"
    ).pack()

    # ================= BUTTON =================
    # tombol untuk mengulang permainan
    tk.Button(
        main,
        text="↻ Coba Lagi",
        bg="#1565D8",
        fg="white",
        font=("Poppins", 10, "bold"),
        width=25,
        height=2,
        relief="flat",
        cursor="hand2"
    ).pack(pady=(25, 10))

    # tombol untuk kembali ke menu utama
    tk.Button(
        main,
        text="☰ Menu Utama",
        bg="white",
        fg="#1565D8",
        font=("Poppins", 10),
        width=25,
        height=2,
        relief="solid",
        cursor="hand2"
        # TODO : MENAMBAHKAN COMMAND UNTUK BALIK KE MENU SCREEN
    ).pack()


# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Game Over")
#     root.geometry("800x600")

#     tampil(root)

#     root.mainloop()
