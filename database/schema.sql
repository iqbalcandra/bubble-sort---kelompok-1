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
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    tanggal_daftar DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- TABEL LEVELS
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS levels (
    id_level INT PRIMARY KEY AUTO_INCREMENT,
    nama_level VARCHAR(20) NOT NULL,
    jumlah_warna INT NOT NULL,
    jumlah_tabung INT NOT NULL,
    timer INT NOT NULL,
    skor_dasar INT NOT NULL
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- TABEL SCORES
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS scores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    score INT NOT NULL,
    level_reached VARCHAR(20) NOT NULL,
    tanggal_main DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- TABEL PROGRESS
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS progress (
    id_progress INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    current_level VARCHAR(20) DEFAULT 'Easy',
    best_score INT DEFAULT 0,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;