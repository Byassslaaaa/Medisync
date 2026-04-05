-- Script inisialisasi dua database PostgreSQL yang terpisah
-- Dijalankan otomatis oleh Docker saat container postgres pertama kali dibuat

CREATE DATABASE db_pendaftaran;
CREATE DATABASE db_rekam_medis;

\connect db_pendaftaran
CREATE EXTENSION IF NOT EXISTS pgcrypto;

\connect db_rekam_medis
CREATE EXTENSION IF NOT EXISTS pgcrypto;
