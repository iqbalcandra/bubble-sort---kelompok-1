"""
theme.py
Konstanta warna, font, dan ukuran window bersama untuk seluruh screens/.

Sebelumnya tiap file screen (game_screen.py, login_screen.py, menu_screen.py)
punya konstanta warna sendiri-sendiri yang saling beda (mis. BG_COLOR
"#F1F2FB" vs "#F8F9FF" vs "#F9F9FF"). File ini jadi SATU sumber acuan,
supaya tampilan konsisten di semua screen.
"""

# ---------------------------------------------------------------------------
# Ukuran window aplikasi (fixed, tidak bisa di-resize) — sesuai desain UI/UX
# ---------------------------------------------------------------------------
LEBAR_WINDOW = 1440
TINGGI_WINDOW = 1024

# ---------------------------------------------------------------------------
# Palet warna utama
# ---------------------------------------------------------------------------
BG_COLOR = "#F8F9FF"          # background utama (dipakai semua screen)
CARD_COLOR = "#FFFFFF"        # warna card/panel putih
AREA_CARD_COLOR = "#D9D9D9"   # card abu-abu (khusus area permainan game_screen.py)

PRIMARY_BLUE = "#2170E4"
PRIMARY_BLUE_DARK = "#1E3A8A"
PRIMARY_BLUE_LIGHT = "#4A8DEC"

TEXT_DARK = "#191B23"
TEXT_MUTED = "#5D5F5F"

DANGER_BG = "#FFDAD6"
DANGER_TEXT = "#BA1A1A"

# Warna badge per tingkat kesulitan level
LEVEL_BADGE_COLOR = {
    "Mudah": "#2170E4",
    "Sedang": "#B45309",
    "Sulit": "#B91C1C",
}

# ---------------------------------------------------------------------------
# Font
# ---------------------------------------------------------------------------
FONT_KELUARGA = "Segoe UI"


def font(ukuran: int = 11, tebal: bool = False) -> tuple:
    """
    Helper membuat tuple font Tkinter yang konsisten.
    Contoh: font(18, tebal=True) -> ("Segoe UI", 18, "bold")
    """
    return (FONT_KELUARGA, ukuran, "bold" if tebal else "normal")

