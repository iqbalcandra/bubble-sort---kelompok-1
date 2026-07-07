import tkinter as tk
from tkinter import ttk


def tampil(parent):

    # Hapus halaman sebelumnya
    for widget in parent.winfo_children():
        widget.destroy()

    # mengatur warna background halaman
    parent.configure(bg="#F6F6F6")

    # ================= MAIN =================
    # frame utama untuk menampung semua widget
    main = tk.Frame(parent, bg="#F6F6F6")
    main.pack(fill="both", expand=True, padx=30, pady=20)

    # ================= HEADER =================
    # berisi tombol kembali ke halaman progres
    header = tk.Frame(main, bg="#F6F6F6")
    header.pack(fill="x")

    tk.Button(
        header,
        text="← Progres",
        relief="flat",
        bg="#F6F6F6",
        fg="#0057C8",
        font=("Poppins", 11, "bold")
    ).pack(side="left")

    # ================= CARD ATAS =================
    # untuk menampilkan level terakhir dan skor terbaik
    atas = tk.Frame(main, bg="#F6F6F6")
    atas.pack(fill="x", pady=20)

    # ------------ LEVEL ------------
    level = tk.Frame(
        atas,
        bg="white",
        highlightbackground="#1565C0",
        highlightthickness=1,
        width=330,
        height=120
    )
    level.pack(side="left")
    level.pack_propagate(False)

    # judul card level
    tk.Label(level, text="LEVEL TERAKHIR",
             bg="white",
             fg="gray",
             font=("Poppins", 8)).pack(anchor="w", padx=12, pady=(10, 0))

    # level terakhir pemain bermain
    tk.Label(level, text="Medium",
             bg="white",
             fg="#1565C0",
             font=("Poppins", 20, "bold")).pack(anchor="w", padx=12)

    # keterangan target level berikutnya
    tk.Label(level, text="Menuju Hard",
             bg="white",
             fg="gray",
             font=("Poppins", 8)).pack(anchor="w", padx=12, pady=(5, 0))

    # progres menuju level berikutnya
    progress = ttk.Progressbar(level, length=160, value=85)
    progress.pack(anchor="w", padx=12, pady=5)

    # persentase progres
    tk.Label(level, text="85%",
             bg="white",
             fg="#1565C0",
             font=("Poppins", 8, "bold")).place(x=250, y=82)

    # ------------ SKOR ------------
    skor = tk.Frame(
        atas,
        bg="#1565C0",
        width=460,
        height=120
    )

    skor.pack(side="left", padx=15)
    skor.pack_propagate(False)

    # judul card skor
    tk.Label(
        skor,
        text="SKOR TERBAIK",
        bg="#1565C0",
        fg="white",
        font=("Poppins", 8)
    ).pack(anchor="w", padx=15, pady=(10, 0))

    # card untuk skor terbaik dan peringkat di leaderboard
    tk.Label(
        skor,
        text="2.450",
        bg="#1565C0",
        fg="white",
        font=("Poppins", 24, "bold")
    ).pack(anchor="w", padx=15)

    tk.Label(
        skor,
        text="🏆 Peringkat #5 di Leaderboard",
        bg="#1565C0",
        fg="white",
        font=("Poppins", 9)
    ).pack(anchor="w", padx=15, pady=8)

    # ================= TENGAH =================
    # berisi ringkasan bermain, target berikutnya, dan riwayat permainan
    tengah = tk.Frame(main, bg="#F6F6F6")
    tengah.pack(pady=10)

    # Ringkasan
    ringkasan = tk.Frame(
        tengah,
        bg="white",
        width=280,
        height=180,
        highlightbackground="#DDDDDD",
        highlightthickness=1
    )

    ringkasan.pack(side="left")
    ringkasan.pack_propagate(False)

    tk.Label(
        ringkasan,
        text="Ringkasan Bermain",
        bg="white",
        font=("Poppins", 11, "bold")
    ).pack(anchor="w", padx=12, pady=10)

    kotak1 = tk.Frame(ringkasan, bg="#F3F5FF")
    kotak1.pack(fill="x", padx=12, pady=5)

    tk.Label(kotak1, text="🕒", bg="#1565C0", fg="white",
             width=2).pack(side="left", padx=6, pady=8)

    tk.Label(
        kotak1,
        text="Total Waktu\n24j 15m",
        justify="left",
        bg="#F3F5FF",
        font=("Poppins", 9)
    ).pack(anchor="w", padx=10)

    kotak2 = tk.Frame(ringkasan, bg="#F3F5FF")
    kotak2.pack(fill="x", padx=12, pady=5)

    tk.Label(kotak2, text="✓", bg="#1565C0", fg="white",
             width=2).pack(side="left", padx=6, pady=8)

    tk.Label(
        kotak2,
        text="Level Selesai\nMedium",
        justify="left",
        bg="#F3F5FF",
        font=("Poppins", 9)
    ).pack(anchor="w", padx=10)

    # Target
    target = tk.Frame(
        tengah,
        bg="#E9EAF4",
        width=280,
        height=180
    )

    target.pack(side="left")
    target.pack_propagate(False)

    tk.Label(
        target,
        text="Target Berikutnya",
        bg="#E9EAF4",
        font=("Poppins", 11, "bold")
    ).pack(pady=(35, 10))

    tk.Label(
        target,
        text="Selesaikan Hard Mode",
        bg="#E9EAF4",
        fg="gray",
        font=("Poppins", 9)
    ).pack()

    tk.Button(
        target,
        text="Lanjut Bermain",
        bg="#1565C0",
        fg="white",
        relief="flat",
        width=18
    ).pack(pady=25)

    # ================= RIWAYAT =================
    bawah = tk.Frame(
        main,
        bg="white",
        highlightbackground="#DDDDDD",
        highlightthickness=1
    )

    bawah.pack(fill="x", pady=20)

    header2 = tk.Frame(bawah, bg="#F4F6FF")
    header2.pack(fill="x")

    tk.Label(
        header2,
        text="Riwayat Permainan",
        bg="#F4F6FF",
        font=("Poppins", 10, "bold")
    ).pack(side="left", padx=10, pady=8)

    tk.Label(
        header2,
        text="Lihat Semua",
        bg="#F4F6FF",
        fg="#1565C0",
        font=("Poppins", 8)
    ).pack(side="right", padx=10)

    # data = [
    #     ("✔","Medium - Berhasil","Hari ini, 14:20","450 Pts","03:45"),
    #     ("✔","Easy - Berhasil","Kemarin, 18:12","420 Pts","04:12")
    # ]

    # for status, level, waktu, skor, durasi in data:

    #     baris = tk.Frame(bawah, bg="white")
    #     baris.pack(fill="x", padx=10, pady=8)

    #     tk.Label(baris, text=status, bg="#DFF7E2", width=2).pack(side="left")

    #     info = tk.Frame(baris, bg="white")
    #     info.pack(side="left", padx=10)

    #     tk.Label(info, text=level, bg="white",
    #              font=("Poppins", 9, "bold")).pack(anchor="w")

    #     tk.Label(info, text=waktu, bg="white",
    #              fg="gray", font=("Poppins", 8)).pack(anchor="w")

    #     tk.Label(baris, text=skor, bg="white",
    #              font=("Poppins", 9, "bold")).pack(side="right", padx=20)

    #     tk.Label(baris, text=durasi, bg="white",
    #              fg="gray", font=("Poppins", 8)).pack(side="right")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Game Over")
    root.geometry("800x600")

    tampil(root)

    root.mainloop()
