"""
timer_manager.py
Mengelola countdown timer per level permainan.

Timer berjalan mundur sejak level dimulai, ditampilkan real-time di layar
permainan (game_screen.py), dan otomatis memicu Game Over saat mencapai 0.
Sisa waktu saat level selesai digunakan sebagai dasar bonus skor
(lihat score_manager.py).
"""


class TimerManager:
    def __init__(self, widget, durasi_detik: int, on_tick=None, on_timeout=None):
        """
        :param widget: widget Tkinter (root/frame) yang punya method .after()
                        digunakan untuk menjadwalkan tick tiap 1 detik
        :param durasi_detik: durasi awal timer level (dari tabel levels, kolom timer)
        :param on_tick: callback(sisa_waktu) dipanggil tiap 1 detik, untuk update label
        :param on_timeout: callback() dipanggil saat waktu habis (sisa_waktu == 0)
        """
        self.widget = widget
        self.durasi_awal = durasi_detik
        self.sisa_waktu = durasi_detik
        self.on_tick = on_tick
        self.on_timeout = on_timeout

        self._job_id = None       # id job dari widget.after(), untuk keperluan cancel
        self._berjalan = False

    def mulai(self) -> None:
        """Memulai countdown timer dari durasi awal."""
        self.sisa_waktu = self.durasi_awal
        self._berjalan = True
        self._jadwalkan_tick()

    def _jadwalkan_tick(self) -> None:
        if not self._berjalan:
            return
        self._job_id = self.widget.after(1000, self._tick)

    def _tick(self) -> None:
        if not self._berjalan:
            return

        self.sisa_waktu -= 1

        if self.on_tick:
            self.on_tick(self.sisa_waktu)

        if self.sisa_waktu <= 0:
            self.berhenti()
            if self.on_timeout:
                self.on_timeout()
            return

        self._jadwalkan_tick()

    def berhenti(self) -> None:
        """Menghentikan timer (dipanggil saat level selesai/menang, atau timeout)."""
        self._berjalan = False
        if self._job_id is not None:
            self.widget.after_cancel(self._job_id)
            self._job_id = None

    def reset(self) -> None:
        """
        Mengulang timer ke durasi awal. Dipanggil saat pemain menekan
        tombol 'Ulangi Level' (fitur Reset Level di laporan BAB 5.5).
        """
        self.berhenti()
        self.sisa_waktu = self.durasi_awal

    def get_sisa_waktu(self) -> int:
        """Mengembalikan sisa waktu saat ini dalam detik."""
        return max(self.sisa_waktu, 0)

    def get_format_waktu(self) -> str:
        """Mengembalikan sisa waktu dalam format MM:SS untuk ditampilkan di UI."""
        menit = self.sisa_waktu // 60
        detik = self.sisa_waktu % 60
        return f"{menit:02d}:{detik:02d}"
