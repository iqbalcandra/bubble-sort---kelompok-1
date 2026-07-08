-- ============================================================
-- SCHEMA DATABASE - COLOR BALL SORT PUZZLE
-- ============================================================

CREATE DATABASE IF NOT EXISTS color_ball_sort
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE color_ball_sort;

-- ------------------------------------------------------------
-- TABEL USERS
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    tanggal_daftar DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- TABEL LEVELS
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS levels (
    id_level INT AUTO_INCREMENT PRIMARY KEY,
    nama_level VARCHAR(20) NOT NULL UNIQUE,
    jumlah_warna INT NOT NULL,
    jumlah_tabung INT NOT NULL,
    timer INT NOT NULL,
    skor_dasar INT NOT NULL
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- TABEL SCORES
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    score INT NOT NULL,
    level_reached VARCHAR(20) NOT NULL,
    waktu_bermain DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_scores_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- TABEL PROGRESS
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS progress (
    id_progress INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL UNIQUE,

    current_level VARCHAR(20) NOT NULL DEFAULT 'Mudah',

    best_score INT NOT NULL DEFAULT 0,

    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_progress_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;
