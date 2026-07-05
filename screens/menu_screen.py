import tkinter as tk
from tkinter import messagebox


class MenuScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Ball Sort Puzzle - Menu")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#87CEEB")

        # Judul
        judul = tk.Label(
            self.root,
            text="COLOR BALL SORT PUZZLE",
            font=("Arial", 24, "bold"),
            bg="#87CEEB",
            fg="white"
        )
        judul.pack(pady=40)

        # Sub Judul
        subjudul = tk.Label(
            self.root,
            text="Main Menu",
            font=("Arial", 14),
            bg="#87CEEB",
            fg="white"
        )
        subjudul.pack(pady=5)

        # Frame tombol
        frame = tk.Frame(self.root, bg="#87CEEB")
        frame.pack(pady=30)

        # Tombol Mulai Game
        btn_mulai = tk.Button(
            frame,
            text="Mulai Game",
            width=20,
            height=2,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.mulai_game
        )
        btn_mulai.pack(pady=10)

        # Tombol Leaderboard
        btn_leaderboard = tk.Button(
            frame,
            text="Leaderboard",
            width=20,
            height=2,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.buka_leaderboard
        )
        btn_leaderboard.pack(pady=10)

        # Tombol Pengaturan
        btn_pengaturan = tk.Button(
            frame,
            text="Pengaturan",
            width=20,
            height=2,
            bg="#FFC107",
            font=("Arial", 12, "bold"),
            command=self.buka_pengaturan
        )
        btn_pengaturan.pack(pady=10)

        # Tombol Keluar
        btn_keluar = tk.Button(
            frame,
            text="Keluar",
            width=20,
            height=2,
            bg="#F44336",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.keluar_game
        )
        btn_keluar.pack(pady=10)

        # Footer
        footer = tk.Label(
            self.root,
            text="Kelompok 1 | Algoritma dan Pemrograman 2",
            font=("Arial", 10),
            bg="#87CEEB",
            fg="white"
        )
        footer.pack(side="bottom", pady=15)

    # ==========================
    # Fungsi Tombol
    # ==========================

    def mulai_game(self):
        """
        Nanti diarahkan ke level_screen.py
        """
        messagebox.showinfo(
            "Mulai Game",
            "Halaman pemilihan level akan dibuka."
        )

        # Contoh jika level_screen.py sudah selesai
        # self.root.destroy()
        # import level_screen

    def buka_leaderboard(self):
        """
        Nanti diarahkan ke leaderboard_screen.py
        """
        try:
            self.root.destroy()
            import leaderboard_screen
        except ModuleNotFoundError:
            messagebox.showinfo(
                "Leaderboard",
                "Halaman leaderboard belum tersedia."
            )

    def buka_pengaturan(self):
        messagebox.showinfo(
            "Pengaturan",
            "Fitur pengaturan masih dalam pengembangan."
        )

    def keluar_game(self):
        konfirmasi = messagebox.askyesno(
            "Keluar",
            "Apakah Anda yakin ingin keluar?"
        )

        if konfirmasi:
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MenuScreen(root)
    root.mainloop()
