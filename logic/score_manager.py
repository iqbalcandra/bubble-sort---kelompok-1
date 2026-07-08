from database.queries import simpan_skor


class ScoreManager:

    def __init__(self):

        self.level_data = None
        self.base_score = 0
        self.bonus_waktu = 0
        self.total_score = 0


    def set_level(self, level_data):

        self.level_data = level_data

        self.total_score = 0
        self.bonus_waktu = 0

        nama = level_data["nama_level"]

        if nama == "Mudah":
            self.base_score = 100

        elif nama == "Sedang":
            self.base_score = 250

        elif nama == "Sulit":
            self.base_score = 500

        else:
            self.base_score = 100


    # ==========================================
    # HITUNG SKOR
    # ==========================================

    def hitung_skor(self, sisa_waktu):

        """
        Menghitung skor akhir.

        Rumus:

        Skor =
        Skor Dasar Level +
        Bonus Waktu

        Bonus waktu:
        10 poin / detik
        """


        self.bonus_waktu = sisa_waktu * 10


        self.total_score = (
            self.base_score +
            self.bonus_waktu
        )


        return self.total_score




    # ==========================================
    # SIMPAN SKOR DATABASE
    # ==========================================

    def simpan_skor(
            self,
            user_id,
            level_reached
    ):

        """
        Menyimpan skor ke tabel scores.
        """


        return simpan_skor(
            user_id=user_id,
            score=self.total_score,
            level_reached=level_reached
        )




    # ==========================================
    # RINCIAN SKOR
    # ==========================================

    def get_rincian_skor(self):


        return {

            "skor_dasar":
                self.base_score,


            "bonus_waktu":
                self.bonus_waktu,


            "total_score":
                self.total_score

        }
