import tkinter as tk
from tkinter import messagebox


class MenuScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Ball Sort Puzzle")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#87CEEB")

        # Judul
        title = tk.Label(
            root,
            text="COLOR BALL SORT PUZZLE",
            font=("Arial", 24, "bold"),
            bg="#87CEEB",
            fg="white"
        )
        title.pack(pady=50)

        # Frame tombol
        button_frame = tk.Frame(root, bg="#87CEEB")
        button_frame.pack()

        # Tombol Mulai Game
        btn_start = tk.Button(
            button_frame,
            text="Mulai Game",
            width=20,
            height=2,
            font=("Arial", 14),
            command=self.start_game
        )
        btn_start.pack(pady=10)

        # Tombol Leaderboard
        btn_leaderboard = tk.Button(
            button_frame,
            text="Leaderboard",
            width=20,
            height=2,
            font=("Arial", 14),
            command=self.show_leaderboard
        )
        btn_leaderboard.pack(pady=10)

        # Tombol Pengaturan
        btn_settings = tk.Button(
            button_frame,
            text="Pengaturan",
            width=20,
            height=2,
            font=("Arial", 14),
            command=self.settings
        )
        btn_settings.pack(pady=10)

        # Tombol Keluar
        btn_exit = tk.Button(
            button_frame,
            text="Keluar",
            width=20,
            height=2,
            font=("Arial", 14),
            bg="red",
            fg="white",
            command=self.exit_game
        )
        btn_exit.pack(pady=10)

        # Footer
        footer = tk.Label(
            root,
            text="Kelompok 1 - Algoritma dan Pemrograman 2",
            font=("Arial", 10),
            bg="#87CEEB",
            fg="white"
        )
        footer.pack(side="bottom", pady=15)

    # Fungsi tombol sementara
    def start_game(self):
        messagebox.showinfo("Mulai Game", "Masuk ke halaman level")

    def show_leaderboard(self):
        messagebox.showinfo("Leaderboard", "Menampilkan Top 10 skor")

    def settings(self):
        messagebox.showinfo("Pengaturan", "Menu pengaturan")

    def exit_game(self):
        self.root.destroy()


# Testing
if __name__ == "__main__":
    root = tk.Tk()
    app = MenuScreen(root)
    root.mainloop()