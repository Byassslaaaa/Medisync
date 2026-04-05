-- Inisialisasi database untuk Service A (postgres-a)
-- Container postgres-a sudah otomatis membuat database db_pendaftaran
-- via env POSTGRES_DB. Script ini hanya mengaktifkan extension pgcrypto
-- yang diperlukan untuk fungsi gen_random_uuid().

CREATE EXTENSION IF NOT EXISTS pgcrypto;
