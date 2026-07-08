"""
logic/level_manager.py
Mengelola data & urutan level (Mudah -> Sedang -> Sulit), mengambil
konfigurasi level dari database lewat database/queries.py.

API dipakai di screens/game_screen.py:
    level_manager.next_level(id_level)   -> dict level berikutnya, atau None
                                             jika id_level adalah level terakhir
"""

from database import queries


class LevelManager:
    def __init__(self):
        # cache sederhana supaya tidak query berulang kali dalam 1 sesi
        self._levels_cache = None

    def _ambil_semua_level_urut(self) -> list:
        """
        Mengambil seluruh level dari database, diurutkan berdasarkan id_level.
        Di-cache supaya panggilan berulang (next_level, get_level_by_id, dst)
        tidak query database berkali-kali.
        """
        if self._levels_cache is None:
            data = queries.get_all_levels()
            self._levels_cache = sorted(data, key=lambda lvl: lvl["id_level"])
        return self._levels_cache

    def muat_ulang(self) -> None:
        """Membersihkan cache, dipanggil jika data level di database berubah."""
        self._levels_cache = None

    def get_semua_level(self) -> list:
        """Mengembalikan seluruh level, terurut dari Mudah -> Sulit."""
        return self._ambil_semua_level_urut()

    def get_level_by_id(self, id_level: int):
        """Mengambil satu level berdasarkan id_level. Return None jika tidak ada."""
        for lvl in self._ambil_semua_level_urut():
            if lvl["id_level"] == id_level:
                return lvl
        return None

    def get_level_by_name(self, nama_level: str):
        """Mengambil satu level berdasarkan namanya (Mudah/Sedang/Sulit)."""
        for lvl in self._ambil_semua_level_urut():
            if lvl["nama_level"] == nama_level:
                return lvl
        return None

    def next_level(self, id_level: int):
        """
        Mengembalikan dict level berikutnya setelah id_level.
        Dipanggil di game_screen.py (update_player_progress) untuk menentukan
        level_selanjutnya setelah pemain menang.

        :return: dict level berikutnya, atau None jika id_level adalah level
                 terakhir (Sulit) / id_level tidak ditemukan
        """
        levels = self._ambil_semua_level_urut()

        for index, lvl in enumerate(levels):
            if lvl["id_level"] == id_level:
                if index + 1 < len(levels):
                    return levels[index + 1]
                return None  # sudah di level terakhir

        return None  # id_level tidak ditemukan

    def is_level_terakhir(self, id_level: int) -> bool:
        """Mengecek apakah id_level adalah level terakhir (Sulit)."""
        return self.next_level(id_level) is None

    def is_level_terbuka(self, id_level: int, current_level_pemain: str) -> bool:
        """
        Mengecek apakah sebuah level sudah terbuka/bisa dimainkan pemain,
        berdasarkan current_level yang tersimpan di tabel progress.
        Dipakai oleh screens/level_screen.py untuk status lock/unlock.

        Aturan: level terbuka jika id_level <= id dari current_level_pemain.
        """
        levels = self._ambil_semua_level_urut()
        target_level = self.get_level_by_id(id_level)
        pemain_level = self.get_level_by_name(current_level_pemain)

        if target_level is None or pemain_level is None:
            return False

        return target_level["id_level"] <= pemain_level["id_level"]
