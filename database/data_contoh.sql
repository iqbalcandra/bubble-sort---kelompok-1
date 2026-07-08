-- ============================================================
-- COLOR BALL SORT PUZZLE - DATA CONTOH
-- Jalankan setelah schema.sql
-- ============================================================

USE color_ball_sort;

-- ------------------------------------------------------------
-- DATA LEVEL
-- ------------------------------------------------------------
INSERT INTO levels
(nama_level, jumlah_warna, jumlah_tabung, timer, skor_dasar)
VALUES
('Mudah',3,5,120,100),
('Sedang',5,7,90,200),
('Sulit',7,9,60,300)
ON DUPLICATE KEY UPDATE
jumlah_warna=VALUES(jumlah_warna),
jumlah_tabung=VALUES(jumlah_tabung),
timer=VALUES(timer),
skor_dasar=VALUES(skor_dasar);

-- ------------------------------------------------------------
-- DATA USER
-- Password:
-- admin123
-- budi456
-- citra789
-- doni000
--
-- Ganti hash jika menggunakan password yang berbeda.
-- ------------------------------------------------------------

INSERT INTO users
(username,password,tanggal_daftar)
VALUES
(
'admin',
SHA2('admin123',256),
'2026-01-01 08:00:00'
),
(
'budi',
SHA2('budi456',256),
'2026-01-02 09:30:00'
),
(
'citra',
SHA2('citra789',256),
'2026-01-03 14:00:00'
),
(
'doni',
SHA2('doni000',256),
'2026-01-04 10:15:00'
)
ON DUPLICATE KEY UPDATE
username=username;

-- ------------------------------------------------------------
-- DATA SCORES
-- ------------------------------------------------------------

INSERT INTO scores
(user_id,score,level_reached,waktu_bermain)
VALUES
(1,1550,'Sulit','2026-01-05 10:00:00'),
(1,1200,'Sedang','2026-01-06 11:30:00'),
(1,980,'Mudah','2026-01-07 09:00:00'),

(2,850,'Sedang','2026-01-05 13:00:00'),
(2,620,'Mudah','2026-01-06 14:00:00'),
(2,730,'Sedang','2026-01-07 15:00:00'),

(3,450,'Mudah','2026-01-06 16:00:00'),
(3,510,'Mudah','2026-01-07 17:00:00'),
(3,780,'Sedang','2026-01-08 10:00:00'),

(4,320,'Mudah','2026-01-08 11:00:00'),
(4,410,'Mudah','2026-01-09 12:00:00');

-- ------------------------------------------------------------
-- DATA PROGRESS
-- ------------------------------------------------------------

INSERT INTO progress
(user_id,current_level,best_score,last_updated)
VALUES
(1,'Sulit',1550,'2026-01-07 09:00:00'),
(2,'Sedang',850,'2026-01-07 15:00:00'),
(3,'Sedang',780,'2026-01-08 10:00:00'),
(4,'Mudah',410,'2026-01-09 12:00:00')
ON DUPLICATE KEY UPDATE
current_level=VALUES(current_level),
best_score=VALUES(best_score),
last_updated=VALUES(last_updated);
