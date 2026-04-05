-- Inisialisasi database untuk Service B (postgres-b)
-- Container postgres-b sudah otomatis membuat database db_rekam_medis
-- via env POSTGRES_DB. Script ini hanya mengaktifkan extension pgcrypto
-- yang diperlukan untuk fungsi gen_random_uuid().

CREATE EXTENSION IF NOT EXISTS pgcrypto;
