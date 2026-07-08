"""
logic/timer_manager.py
Mengelola countdown timer per level permainan.

Desain: murni logic (TIDAK bergantung pada Tkinter/widget).
Perhitungan sisa waktu berbasis waktu asli (time.time()), sehingga akurat
walau ada jeda/lag pada loop UI. Screen (game_screen.py) yang bertanggung
jawab memanggil get_sisa_waktu() / is_habis() secara berkala (mis. lewat
self.after(1000, ...)) untuk memperbarui tampilan.
"""

import time


class TimerManager:
    def __init__(self):
        self.durasi_awal = 0     # durasi total level (detik)
        self.waktu_mulai = None  # timestamp saat timer mulai berjalan
        self.berjalan = False
        self._sisa_waktu_cache = 0

    def start(self, durasi_detik: int) -> None:
        """
        Memulai countdown dari durasi_detik.
        Dipanggil saat level dimulai / diulang (reset_level -> start_level).
        """
        self.durasi_awal = durasi_detik
        self.waktu_mulai = time.time()
        self.berjalan = True
        self._sisa_waktu_cache = durasi_detik

    def stop(self) -> None:
        """Menghentikan timer (dipanggil saat menang, waktu habis, atau reset)."""
        if self.berjalan:
            # simpan sisa waktu terakhir sebelum berhenti, untuk keperluan skor
            self._sisa_waktu_cache = self.get_sisa_waktu()
        self.berjalan = False

    def get_sisa_waktu(self) -> int:
        """
        Menghitung & mengembalikan sisa waktu (detik) saat ini.
        Dipakai oleh update_timer() di game_screen.py setiap 1 detik,
        dan oleh score_manager saat menghitung bonus waktu.
        """
        if not self.berjalan or self.waktu_mulai is None:
            return self._sisa_waktu_cache

        elapsed = int(time.time() - self.waktu_mulai)
        sisa = self.durasi_awal - elapsed
        if sisa < 0:
            sisa = 0
        self._sisa_waktu_cache = sisa
        return sisa

    def is_habis(self) -> bool:
        """Mengecek apakah waktu sudah habis (dipanggil tiap tick di update_timer())."""
        return self.get_sisa_waktu() <= 0

    def get_format_time(self) -> str:
        """Mengembalikan sisa waktu dalam format MM:SS untuk label WAKTU di UI."""
        sisa = self.get_sisa_waktu()
        menit = sisa // 60
        detik = sisa % 60
        return f"{menit:02d}:{detik:02d}"
