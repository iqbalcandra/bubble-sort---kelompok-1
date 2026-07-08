"""
logic/level_manager.py

Mengatur data level Color Ball Sort Puzzle.

Tugas:
- Mengambil data level dari database
- Mengecek level terbuka / terkunci
- Menentukan level berikutnya
- Mengecek level terakhir

Tidak menggunakan Tkinter.
"""


from database.queries import get_all_levels


class LevelManager:


    def __init__(self):

        self.levels = []

        self.load_levels()



    # ==========================================
    # LOAD LEVEL DARI DATABASE
    # ==========================================

    def load_levels(self):

        """
        Mengambil semua level dari tabel levels.
        """

        self.levels = get_all_levels()



    # ==========================================
    # AMBIL SEMUA LEVEL
    # ==========================================

    def get_semua_level(self):

        """
        Dipakai oleh level_screen.py
        untuk membuat card level.
        """

        return self.levels



    # ==========================================
    # CEK LEVEL TERBUKA
    # ==========================================

    def is_level_terbuka(
            self,
            id_level,
            current_level
    ):

        """
        Sistem unlock:

        Level 1:
        selalu terbuka

        Level berikutnya:
        terbuka jika pemain sudah mencapai level tersebut.
        """


        if isinstance(current_level, str):

            current = self.get_level_by_name(
                current_level
            )

            if current:

                current_level = current["id_level"]

            else:

                current_level = 1



        return id_level <= current_level




    # ==========================================
    # CARI LEVEL BERDASARKAN ID
    # ==========================================

    def get_level_by_id(
            self,
            id_level
    ):


        for level in self.levels:

            if level["id_level"] == id_level:

                return level


        return None



    # ==========================================
    # CARI LEVEL BERDASARKAN NAMA
    # ==========================================

    def get_level_by_name(
            self,
            nama
    ):


        for level in self.levels:

            if level["nama_level"] == nama:

                return level


        return None



    # ==========================================
    # LEVEL BERIKUTNYA
    # ==========================================

    def next_level(
            self,
            id_level
    ):


        next_id = id_level + 1


        return self.get_level_by_id(
            next_id
        )



    # ==========================================
    # CEK LEVEL TERAKHIR
    # ==========================================

    def is_level_terakhir(
            self,
            id_level
    ):


        if len(self.levels) == 0:

            return True



        level_terakhir = max(
            self.levels,
            key=lambda x:x["id_level"]
        )


        return id_level == level_terakhir["id_level"]
