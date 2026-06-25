```python
import tkinter as tk
from tkinter import messagebox


class LevelScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Ball Sort Puzzle - Level")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#87CEEB")

        # Judul
        judul = tk.Label(
            root,
            text="PILIH LEVEL",
            font=("Arial", 24, "bold"),
            bg="#87CEEB",
            fg="white"
        )
        judul.pack(pady=50)

        # Frame tombol
        frame = tk.Frame(root, bg="#87CEEB")
        frame.pack()

        # Level 1
        tk.Button(
            frame,
            text="Level 1",
            width=20,
            height=2,
            font=("Arial", 14),
            command=lambda: self.pilih_level(1)
        ).pack(pady=10)

        # Level 2
        tk.Button(
            frame,
            text="Level 2",
            width=20,
            height=2,
            font=("Arial", 14),
            command=lambda: self.pilih_level(2)
        ).pack(pady=10)

        # Level 3
        tk.Button(
            frame,
            text="Level 3",
            width=20,
            height=2,
            font=("Arial", 14),
            command=lambda: self.pilih_level(3)
        ).pack(pady=10)

        # Tombol Kembali
        tk.Button(
            frame,
            text="Kembali",
            width=20,
            height=2,
            bg="red",
            fg="white",
            font=("Arial", 14),
            command=self.kembali
        ).pack(pady=20)

    # =====================
    # Fungsi
    # =====================

    def pilih_level(self, level):
        messagebox.showinfo(
            "Level",
            f"Anda memilih Level {level}"
        )

        # Nanti diarahkan ke game_screen.py
        # self.root.destroy()
        # import game_screen

    def kembali(self):
        self.root.destroy()

        # Nanti diarahkan ke menu_screen.py
        # import menu_screen


if __name__ == "__main__":
    root = tk.Tk()
    app = LevelScreen(root)
    root.mainloop()
```
