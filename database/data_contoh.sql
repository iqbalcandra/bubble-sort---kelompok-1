-- ============================================================
-- COLOR BALL SORT PUZZLE - Data Contoh
-- Jalankan file ini SETELAH schema.sql
-- ============================================================

USE color_ball_sort;

-- ------------------------------------------------------------
-- DATA LEVEL
-- ------------------------------------------------------------
INSERT INTO levels (nama_level, jumlah_warna, jumlah_tabung, timer, skor_dasar)
VALUES
    ('Easy',   3, 5, 120, 100),
    ('Medium', 5, 7,  90, 200),
    ('Hard',   7, 9,  60, 300)
ON DUPLICATE KEY UPDATE
    jumlah_warna  = VALUES(jumlah_warna),
    jumlah_tabung = VALUES(jumlah_tabung),
    timer         = VALUES(timer),
    skor_dasar    = VALUES(skor_dasar);


-- ------------------------------------------------------------
-- DATA USER CONTOH
-- Password: admin123, budi456, citra789, doni000
-- (di aplikasi di-hash oleh Python hashlib SHA-256)
-- ------------------------------------------------------------
INSERT INTO users (username, password, tanggal_daftar)
VALUES
    ('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831186422d32c5e25e78b2d5', '2025-01-01 08:00:00'),
    ('budi',  '9a0e7cb44b67e762611c7bbcfbbd70f5cd8cc8e0e07b8a6b9a0ebe21d0f5c4a', '2025-01-02 09:30:00'),
    ('citra', 'a3f5c8e1b29d47f06a3e9b12c84f7d2e5b0a1c3d6e8f9b2a4c7d0e3f6a9b2c5', '2025-01-03 14:00:00'),
    ('doni',  '1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b', '2025-01-04 10:15:00');


-- ------------------------------------------------------------
-- DATA SCORES CONTOH
-- ------------------------------------------------------------
INSERT INTO scores (user_id, score, level_reached, tanggal_main)
VALUES
    (1, 1550, 'Hard',   '2025-01-05 10:00:00'),
    (1, 1200, 'Medium', '2025-01-06 11:30:00'),
    (1,  980, 'Easy',   '2025-01-07 09:00:00'),
    (2,  850, 'Medium', '2025-01-05 13:00:00'),
    (2,  620, 'Easy',   '2025-01-06 14:00:00'),
    (2,  730, 'Medium', '2025-01-07 15:00:00'),
    (3,  450, 'Easy',   '2025-01-06 16:00:00'),
    (3,  510, 'Easy',   '2025-01-07 17:00:00'),
    (3,  780, 'Medium', '2025-01-08 10:00:00'),
    (4,  320, 'Easy',   '2025-01-08 11:00:00'),
    (4,  410, 'Easy',   '2025-01-09 12:00:00');


-- ------------------------------------------------------------
-- DATA PROGRESS CONTOH
-- ------------------------------------------------------------
INSERT INTO progress (user_id, current_level, best_score, last_updated)
VALUES
    (1, 'Hard',   1550, '2025-01-07 09:00:00'),
    (2, 'Medium',  850, '2025-01-07 15:00:00'),
    (3, 'Medium',  780, '2025-01-08 10:00:00'),
    (4, 'Easy',    410, '2025-01-09 12:00:00')
ON DUPLICATE KEY UPDATE
    current_level = VALUES(current_level),
    best_score    = VALUES(best_score),
    last_updated  = VALUES(last_updated);