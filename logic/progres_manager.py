"""
logic/progress_manager.py

Mengatur progress pemain Color Ball Sort Puzzle.

Tugas:
- Mengambil progress pemain dari database
- Menyimpan level terakhir yang terbuka
- Menyimpan skor terbaik

Tidak menggunakan Tkinter.
"""


from database.queries import (
    get_progress,
    update_progress as update_db_progress
)


class ProgressManager:

    def __init__(self):

        pass

    # ==========================================
    # AMBIL PROGRESS PEMAIN
    # ==========================================

    def get_progress_pemain(
            self,
            user_id
    ):
        """
        Mengambil progress pemain dari database.

        Return:
        {
            user_id,
            current_level,
            best_score
        }
        """

        return get_progress(
            user_id
        )

    # ==========================================
    # UPDATE PROGRESS
    # ==========================================

    def update_progress(
            self,
            user_id,
            next_level,
            score
    ):
        """
        Update progress setelah pemain menyelesaikan level.

        Parameter:
        user_id    : ID pemain
        next_level : level yang akan dibuka
        score      : skor terakhir

        Sistem:
        - Membandingkan skor lama
        - Menyimpan skor terbesar
        - Membuka level berikutnya
        """

        progress = get_progress(
            user_id
        )

        # Ambil skor terbaik sebelumnya

        if progress:

            old_score = progress.get(
                "best_score",
                0
            )

        else:

            old_score = 0

        # Ambil skor terbesar

        best_score = max(
            old_score,
            score
        )

        # Simpan ke database

        return update_db_progress(
            user_id=user_id,
            current_level=next_level,
            best_score=best_score
        )

    # ==========================================
    # AMBIL LEVEL SEKARANG
    # ==========================================

    def get_current_level(
            self,
            user_id
    ):
        """
        Mengambil level terakhir pemain.
        """

        progress = get_progress(
            user_id
        )

        if progress:

            return progress.get(
                "current_level",
                "Mudah"
            )

        return "Mudah"

    # ==========================================
    # AMBIL SKOR TERBAIK
    # ==========================================

    def get_best_score(
            self,
            user_id
    ):
        """
        Mengambil skor terbaik pemain.
        """

        progress = get_progress(
            user_id
        )

        if progress:

            return progress.get(
                "best_score",
                0
            )

        return 0

    # ==========================================
    # RESET PROGRESS
    # ==========================================

    def reset_progress(
            self,
            user_id
    ):
        """
        Mengembalikan progress pemain
        ke level awal.
        """

        return update_db_progress(
            user_id=user_id,
            current_level="Mudah",
            best_score=0
        )
