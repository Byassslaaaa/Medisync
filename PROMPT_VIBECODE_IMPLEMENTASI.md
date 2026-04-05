PROMPT VIBE CODE - IMPLEMENTASI SOURCE CODE MEDISYNC

Konteks:
Saya mahasiswa yang mengerjakan tugas Jaringan Komputer Terapan.
Judul tugas: Implementasi Komunikasi Microservices.
Saya sudah punya project folder dengan struktur:
- frontend
- service-a
- service-b
- proto
- docker-compose.yml
- init-db.sql

Tujuan:
Tolong audit dan rapikan seluruh source code agar sinkron dengan requirement tugas dan siap demo tanpa error.

Requirement wajib (harus dipenuhi semua):
1. Arsitektur Microservices
- Frontend: input data pasien.
- Service A (Pendaftaran): simpan data pasien, DB sendiri.
- Service B (Rekam Medis): simpan histori/draft rekam medis, DB sendiri.

2. Komunikasi antar layanan
- gRPC (Synchronous): Service A memanggil Service B untuk validasi real-time.
- Message Queue RabbitMQ (Asynchronous): event patient.registered dari Service A dikirim ke Service B.

3. Ketentuan Integrasi
- Database Isolation: Service A tidak boleh query DB Service B, dan sebaliknya.
- Contract-First: gunakan proto/medical_record.proto sebagai kontrak gRPC.

4. Alur fungsional utama
- Frontend submit pasien ke Service A.
- Service A validasi input.
- Service A gRPC CheckPatientRecord(nik) ke Service B.
- Jika belum ada record: Service A simpan ke db_pendaftaran.
- Service A publish event patient.registered ke RabbitMQ.
- Service B consume event dan membuat draft di db_rekam_medis.

5. Endpoint minimum
- Service A:
  - POST /api/patients
  - GET /api/patients
  - GET /health
- Service B:
  - GET /api/records
  - GET /api/records/:nik
  - GET /health

6. Database dan inisialisasi
- PostgreSQL dengan dua DB terpisah:
  - db_pendaftaran
  - db_rekam_medis
- Pastikan extension UUID aktif (pgcrypto) di kedua DB.

7. Docker Compose
- Service: frontend, service-a, service-b, postgres, rabbitmq.
- Tambahkan healthcheck dan depends_on yang masuk akal.
- Port yang jelas untuk demo.

8. Kualitas implementasi
- Logging jelas untuk alur gRPC dan MQ.
- Retry koneksi DB dan RabbitMQ saat startup.
- Error handling yang benar (bedakan data tidak ditemukan vs error DB).

Tugas yang harus kamu lakukan:
A. Lakukan code review seluruh project dan identifikasi gap terhadap requirement.
B. Perbaiki file yang perlu diperbaiki.
C. Jangan ubah arsitektur dasar jika sudah benar.
D. Pastikan semua perubahan konsisten antar service.
E. Hasil akhir harus bisa dijalankan dengan docker compose up --build.

Output yang saya minta:
1. Ringkasan perubahan (file apa saja diubah dan alasannya).
2. Source code final yang sudah diperbaiki.
3. Checklist verifikasi requirement (centang per requirement).
4. Langkah demo end-to-end dari input pasien sampai draft rekam medis terbentuk.
5. Daftar risiko kecil yang tersisa dan cara mitigasinya.
