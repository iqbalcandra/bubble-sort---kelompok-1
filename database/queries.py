"""
database/queries.py

Kumpulan query database Color Ball Sort Puzzle.

Mengatur:
- User login/register
- Level
- Score
- Leaderboard
- Progress pemain
"""

import hashlib

from database.connection import get_connection


# =====================================================
# KONFIGURASI
# =====================================================

LEVEL_AWAL_DEFAULT = "Mudah"



# =====================================================
# UTIL
# =====================================================

def hash_password(password: str):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()



# =====================================================
# USER
# =====================================================


def register_user(username, password):

    conn = get_connection()

    if conn is None:
        return False, "Database tidak terhubung."


    cursor = None

    try:

        cursor = conn.cursor()


        # cek username

        cursor.execute(
            """
            SELECT id 
            FROM users
            WHERE username=%s
            """,
            (username,)
        )


        if cursor.fetchone():

            return False, "Username sudah digunakan."



        password_hash = hash_password(password)



        # insert user

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                password
            )

            VALUES
            (
                %s,
                %s
            )
            """,
            (
                username,
                password_hash
            )
        )


        user_id = cursor.lastrowid



        # buat progress awal

        cursor.execute(
            """
            INSERT INTO progress
            (
                user_id,
                current_level,
                best_score
            )

            VALUES
            (
                %s,
                %s,
                %s
            )
            """,
            (
                user_id,
                LEVEL_AWAL_DEFAULT,
                0
            )
        )


        conn.commit()


        return True, "Registrasi berhasil."



    except Exception as e:


        conn.rollback()

        return False, str(e)



    finally:


        if cursor:
            cursor.close()

        conn.close()




def login_user(username, password):


    conn = get_connection()


    if conn is None:
        return False, "Database tidak terhubung."


    cursor = None


    try:


        cursor = conn.cursor(
            dictionary=True
        )


        password_hash = hash_password(
            password
        )


        cursor.execute(
            """
            SELECT
            id,
            username,
            tanggal_daftar

            FROM users

            WHERE username=%s
            AND password=%s
            """,
            (
                username,
                password_hash
            )
        )


        user = cursor.fetchone()



        if user:

            return True,user


        return False,"Username atau password salah."



    except Exception as e:

        return False,str(e)



    finally:

        if cursor:
            cursor.close()

        conn.close()





# =====================================================
# LEVEL
# =====================================================


def get_all_levels():


    conn=get_connection()


    if conn is None:
        return []


    cursor=None


    try:


        cursor=conn.cursor(
            dictionary=True
        )


        cursor.execute(
            """
            SELECT *
            FROM levels
            ORDER BY id_level ASC
            """
        )


        return cursor.fetchall()



    except Exception as e:

        print(e)

        return []



    finally:

        if cursor:
            cursor.close()

        conn.close()





def get_level_by_name(nama_level):


    conn=get_connection()


    if conn is None:
        return None



    cursor=None


    try:

        cursor=conn.cursor(
            dictionary=True
        )


        cursor.execute(
            """
            SELECT *
            FROM levels
            WHERE nama_level=%s
            """,
            (nama_level,)
        )


        return cursor.fetchone()



    except Exception as e:

        print(e)

        return None



    finally:

        if cursor:
            cursor.close()

        conn.close()




# =====================================================
# SCORE
# =====================================================


def insert_score(
        user_id,
        score,
        level_reached
):


    conn=get_connection()


    if conn is None:
        return False



    cursor=None


    try:


        cursor=conn.cursor()


        cursor.execute(
            """
            INSERT INTO scores
            (
                user_id,
                score,
                level_reached
            )

            VALUES
            (
                %s,
                %s,
                %s
            )
            """,
            (
                user_id,
                score,
                level_reached
            )
        )


        conn.commit()


        return True



    except Exception as e:


        conn.rollback()


        print(
            "[ERROR INSERT SCORE]",
            e
        )


        return False



    finally:

        if cursor:
            cursor.close()

        conn.close()




def simpan_skor(
        user_id,
        score,
        level_reached
):

    return insert_score(
        user_id,
        score,
        level_reached
    )





def get_top_scores(limit=5):


    conn=get_connection()


    if conn is None:
        return []



    cursor=None


    try:


        cursor=conn.cursor(
            dictionary=True
        )


        cursor.execute(
            """
            SELECT

            s.score,
            s.level_reached,
            s.waktu_bermain,
            u.username


            FROM scores s


            JOIN users u

            ON s.user_id=u.id


            ORDER BY s.score DESC


            LIMIT %s
            """,
            (limit,)
        )


        return cursor.fetchall()



    finally:


        if cursor:
            cursor.close()

        conn.close()





# =====================================================
# PROGRESS
# =====================================================


def get_progress(user_id):


    conn=get_connection()


    if conn is None:
        return None



    cursor=None


    try:


        cursor=conn.cursor(
            dictionary=True
        )


        cursor.execute(
            """
            SELECT *
            FROM progress
            WHERE user_id=%s
            """,
            (user_id,)
        )


        data=cursor.fetchone()



        if data:

            return data



        # jika belum ada

        cursor.execute(
            """
            INSERT INTO progress
            (
                user_id,
                current_level,
                best_score
            )

            VALUES
            (
                %s,
                %s,
                %s
            )
            """,
            (
                user_id,
                LEVEL_AWAL_DEFAULT,
                0
            )
        )


        conn.commit()



        return {

            "user_id":user_id,

            "current_level":LEVEL_AWAL_DEFAULT,

            "best_score":0

        }



    except Exception as e:


        print(e)

        return None



    finally:


        if cursor:
            cursor.close()

        conn.close()





def update_progress(
        user_id,
        current_level,
        best_score
):


    conn=get_connection()


    if conn is None:
        return False



    cursor=None


    try:


        cursor=conn.cursor()


        cursor.execute(
            """
            INSERT INTO progress
            (
                user_id,
                current_level,
                best_score
            )

            VALUES
            (
                %s,
                %s,
                %s
            )


            ON DUPLICATE KEY UPDATE


            current_level = VALUES(current_level),


            best_score =
            GREATEST(
                best_score,
                VALUES(best_score)
            )

            """,
            (
                user_id,
                current_level,
                best_score
            )
        )


        conn.commit()


        return True



    except Exception as e:


        conn.rollback()


        print(
            "[ERROR UPDATE PROGRESS]",
            e
        )


        return False



    finally:


        if cursor:
            cursor.close()

        conn.close()




# =====================================================
# STATISTIK
# =====================================================


def get_total_playtime_seconds(user_id):


    conn=get_connection()


    if conn is None:
        return 0



    cursor=None


    try:


        cursor=conn.cursor(
            dictionary=True
        )


        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM scores
            WHERE user_id=%s
            """,
            (user_id,)
        )


        data=cursor.fetchone()


        return data["total"] if data else 0



    finally:


        if cursor:
            cursor.close()

        conn.close()




# =====================================================
# ALIAS KOMPATIBILITAS
# =====================================================

daftar_user = register_user

ambil_semua_level = get_all_levels

ambil_level_by_nama = get_level_by_name

ambil_leaderboard = get_top_scores

ambil_progress = get_progress
