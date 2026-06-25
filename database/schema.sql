-- Color Ball Sort Puzzle - Database Schema
-- Jalankan file ini terlebih dahulu

CREATE DATABASE IF NOT EXISTS color_ball_sort
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE color_ball_sort;

-- Tabel akun pemain
CREATE TABLE IF NOT EXISTS users (
    id             INT          NOT NULL AUTO_INCREMENT,
    username       VARCHAR(50)  NOT NULL,
    password       VARCHAR(255) NOT NULL,
    tanggal_daftar DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Tabel konfigurasi level
CREATE TABLE IF NOT EXISTS levels (
    id_level      INT         NOT NULL AUTO_INCREMENT,
    nama_level    VARCHAR(20) NOT NULL,
    jumlah_warna  INT         NOT NULL,
    jumlah_tabung INT         NOT NULL,
    timer         INT         NOT NULL,
    skor_dasar    INT         NOT NULL,

    PRIMARY KEY (id_level),
    UNIQUE KEY uq_nama_level (nama_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Tabel riwayat skor pemain
CREATE TABLE IF NOT EXISTS scores (
    id            INT         NOT NULL AUTO_INCREMENT,
    user_id       INT         NOT NULL,
    score         INT         NOT NULL DEFAULT 0,
    level_reached VARCHAR(20) NOT NULL,
    tanggal_main  DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    CONSTRAINT fk_scores_user
        FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Tabel progress pemain
CREATE TABLE IF NOT EXISTS progress (
    id_progress   INT         NOT NULL AUTO_INCREMENT,
    user_id       INT         NOT NULL,
    current_level VARCHAR(20) NOT NULL DEFAULT 'Easy',
    best_score    INT         NOT NULL DEFAULT 0,
    last_updated  DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP
                              ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id_progress),
    UNIQUE KEY uq_progress_user (user_id),
    CONSTRAINT fk_progress_user
        FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Index untuk query leaderboard
CREATE INDEX idx_scores_user    ON scores (user_id);
CREATE INDEX idx_scores_score   ON scores (score DESC);
CREATE INDEX idx_scores_tanggal ON scores (tanggal_main DESC);