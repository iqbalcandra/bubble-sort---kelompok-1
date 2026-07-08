"""
level_screen.py
Halaman "Pilih Tingkat Kesulitan" — menampilkan 3 pilihan level
(Mudah/Sedang/Sulit) sesuai desain UI (kanvas 1440x1024 desktop).
"""

import tkinter as tk
from logic.level_manager import LevelManager
from tkinter import messagebox

from screens.theme import (
    COLOR_BG, COLOR_WHITE, COLOR_PRIMARY, COLOR_PRIMARY_LIGHT,
    COLOR_MEDIUM, COLOR_MEDIUM_LIGHT, COLOR_HARD, COLOR_HARD_LIGHT,
    COLOR_TEXT_DARK, COLOR_TEXT_GRAY, COLOR_BORDER,
    FONT_FAMILY, FONT_TITLE, FONT_SUBTITLE, FONT_LOGO,
    WINDOW_WIDTH, WINDOW_HEIGHT, SIDEBAR_WIDTH,
)

LEVELS_DATA = [
    {
        "id_level": 1,
        "tingkat": "TINGKAT 1",
        "judul": "Mudah",
        "nama_level": "Easy",
        "warna": COLOR_PRIMARY,
        "warna_bg_icon": COLOR_PRIMARY_LIGHT,
        "bintang": 1,
    },
    {
        "id_level": 2,
        "tingkat": "TINGKAT 2",
        "judul": "Sedang",
        "nama_level": "Medium",
        "warna": COLOR_MEDIUM,
        "warna_bg_icon": COLOR_MEDIUM_LIGHT,
        "bintang": 2,
    },
    {
        "id_level": 3,
        "tingkat": "TINGKAT 3",
        "judul": "Sulit",
        "nama_level": "Hard",
        "warna": COLOR_HARD,
        "warna_bg_icon": COLOR_HARD_LIGHT,
        "bintang": 3,
    },
]
class LevelScreen(tk.Frame):
    """
    Frame halaman pilih tingkat kesulitan.
    Bisa dipasang di dalam window utama (main.py) dengan sistem
    berpindah-pindah frame, atau dijalankan berdiri sendiri untuk testing.

    Parameter:
        parent          : widget induk (Tk atau Frame container)
        user_data       : dict berisi info user login, contoh:
                           {"username": "Pemain Muda", "level": 12}
        on_pilih_level  : callback(nama_level: str) dipanggil saat kartu level dipilih
        on_navigate     : callback(tujuan: str) untuk navigasi sidebar
                           (mis. "beranda", "leaderboard", "progress", "keluar")
    """

    def __init__(self, parent, user_data=None, on_pilih_level=None, on_navigate=None):
        super().__init__(parent, bg=COLOR_BG)
        self.user_data = user_data or {"username": "Pemain Muda", "level": 12}
        self.on_pilih_level = on_pilih_level
        self.on_navigate = on_navigate

        self._build_sidebar()
        self._build_main_content()

    # ------------------------------------------------------------
    # SIDEBAR
    # ------------------------------------------------------------
    def _build_sidebar(self):
        sidebar = tk.Frame(self, bg=COLOR_WHITE, width=SIDEBAR_WIDTH)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Profil pemain
        profil_frame = tk.Frame(sidebar, bg=COLOR_WHITE)
        profil_frame.pack(fill="x", padx=24, pady=(28, 20))

        avatar = tk.Label(
            profil_frame, text="🧑", font=(FONT_FAMILY, 22),
            bg=COLOR_PRIMARY_LIGHT, fg=COLOR_PRIMARY,
            width=2, height=1, relief="solid", bd=1,
        )
        avatar.grid(row=0, column=0, rowspan=2, padx=(0, 10))

        tk.Label(
            profil_frame, text=self.user_data.get("username", "Pemain Muda"),
            font=(FONT_FAMILY, 11, "bold"), fg=COLOR_PRIMARY, bg=COLOR_WHITE,
        ).grid(row=0, column=1, sticky="w")
        tk.Label(
            profil_frame, text=f"Level {self.user_data.get('level', 1)}",
            font=(FONT_FAMILY, 9), fg=COLOR_TEXT_GRAY, bg=COLOR_WHITE,
        ).grid(row=1, column=1, sticky="w")

        # Menu navigasi
        self._nav_button(sidebar, "🏠  Beranda", "beranda", active=True)
        self._nav_button(sidebar, "🏆  Papan Peringkat", "leaderboard")
        self._nav_button(sidebar, "🎖  Progress", "progress")

        # Tombol keluar di bagian bawah
        keluar_frame = tk.Frame(sidebar, bg=COLOR_WHITE)
        keluar_frame.pack(side="bottom", fill="x", padx=24, pady=24)
        tk.Button(
            keluar_frame, text="⏻  Keluar", font=(FONT_FAMILY, 10, "bold"),
            fg="#DC2626", bg=COLOR_WHITE, bd=0, cursor="hand2",
            activebackground=COLOR_WHITE, activeforeground="#DC2626",
            anchor="w", command=lambda: self._navigate("keluar"),
        ).pack(fill="x")

    def _nav_button(self, parent, text, target, active=False):
        bg = COLOR_PRIMARY if active else COLOR_WHITE
        fg = COLOR_WHITE if active else COLOR_TEXT_DARK
        btn = tk.Button(
            parent, text=text, font=(FONT_FAMILY, 11, "bold" if active else "normal"),
            bg=bg, fg=fg, bd=0, anchor="w", padx=16, pady=10, cursor="hand2",
            activebackground=bg, activeforeground=fg,
            command=lambda: self._navigate(target),
        )
        btn.pack(fill="x", padx=16, pady=3)

    def _navigate(self, target):
        if target == "keluar":
            jawab = messagebox.askyesno("Keluar", "Apakah kamu yakin ingin keluar?")
            if not jawab:
                return
        if self.on_navigate:
            self.on_navigate(target)

    # ------------------------------------------------------------
    # MAIN CONTENT
    # ------------------------------------------------------------
    def _build_main_content(self):
        content = tk.Frame(self, bg=COLOR_BG)
        content.pack(side="left", fill="both", expand=True)

        # Judul
        tk.Label(
            content, text="Pilih Tingkat Kesulitan",
            font=FONT_TITLE, bg=COLOR_BG, fg=COLOR_TEXT_DARK,
        ).pack(pady=(70, 6))

        tk.Label(
            content, text="Tentukan tantanganmu hari ini dan mulailah bermain!",
            font=FONT_SUBTITLE, bg=COLOR_BG, fg=COLOR_TEXT_GRAY,
        ).pack()

        # Container kartu level
        card_container = tk.Frame(content, bg=COLOR_BG)
        card_container.pack(pady=60)

        for data in LEVELS_DATA:
            self._buat_card(card_container, data)

    def _buat_card(self, parent, data):
        card = tk.Frame(
            parent, bg=COLOR_WHITE, width=260, height=340,
            highlightbackground=COLOR_BORDER, highlightthickness=1,
        )
        card.pack(side="left", padx=18)
        card.pack_propagate(False)

        # Ikon bintang dalam lingkaran
        icon_wrap = tk.Label(
            card, text="★" * data["bintang"],
            font=(FONT_FAMILY, 16, "bold"),
            bg=data["warna_bg_icon"], fg=data["warna"],
            width=4, height=2,
        )
        icon_wrap.pack(pady=(30, 14))

        # Badge tingkat
        badge = tk.Label(
            card, text=data["tingkat"], font=(FONT_FAMILY, 8, "bold"),
            bg=data["warna_bg_icon"], fg=data["warna"], padx=10, pady=3,
        )
        badge.pack(pady=(0, 8))

        # Judul level
        tk.Label(
            card, text=data["judul"], font=(FONT_FAMILY, 20, "bold"),
            bg=COLOR_WHITE, fg=COLOR_TEXT_DARK,
        ).pack()

        # Deskripsi
        tk.Label(
            card, text=data["deskripsi"], font=(FONT_FAMILY, 9),
            bg=COLOR_WHITE, fg=COLOR_TEXT_GRAY, justify="center", wraplength=210,
        ).pack(pady=(10, 0))

        # Tombol pilih
        tk.Button(
            card, text=f"Pilih {data['judul']}", font=(FONT_FAMILY, 10, "bold"),
            bg=data["warna"], fg=COLOR_WHITE, bd=0, pady=10, cursor="hand2",
            activebackground=data["warna"], activeforeground=COLOR_WHITE,
            command=lambda d=data: self._pilih(d["id_level"]),
        ).pack(side="bottom", fill="x", padx=24, pady=24)


    def _pilih(self, id_level):

        level_manager = LevelManager()

        level_data = level_manager.get_level(id_level)

        if level_data is None:
            messagebox.showerror("Error", "Data level tidak ditemukan.")
            return

        if self.on_pilih_level:
            self.on_pilih_level(level_data)
        else:
            messagebox.showinfo(
                "Level Dipilih",
                f"Anda memilih Level {level_data['id_level']} ({level_data['nama_level']})"
            )

# ------------------------------------------------------------
# MODE STANDALONE (untuk testing langsung tanpa main.py)
# ------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pilih Tingkat Kesulitan")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.resizable(False, False)
    root.configure(bg=COLOR_BG)

    def contoh_pilih_level(nama_level):
        messagebox.showinfo("Level Dipilih", f"Anda memilih tingkat kesulitan {nama_level}")

    def contoh_navigate(target):
        if target == "keluar":
            root.destroy()
        else:
            messagebox.showinfo("Navigasi", f"Pindah ke halaman: {target}")

    screen = LevelScreen(
        root,
        user_data={"username": "Pemain Muda", "level": 12},
        on_pilih_level=contoh_pilih_level,
        on_navigate=contoh_navigate,
    )
    screen.pack(fill="both", expand=True)

    root.mainloop()