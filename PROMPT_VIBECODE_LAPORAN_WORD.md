PROMPT VIBE CODE - GENERATE DOKUMEN WORD LAPORAN LENGKAP

Konteks:
Saya sudah memiliki project microservices MediSync (Frontend, Service A, Service B, gRPC, RabbitMQ, PostgreSQL terpisah).
Tolong buatkan dokumen laporan lengkap dalam format Word (.docx) yang siap dikumpulkan.
Bahasa: Indonesia mahasiswa, natural, jelas, tidak terlalu kaku.

Judul tugas:
Implementasi Komunikasi Microservices

Capaian pembelajaran yang wajib dicantumkan:
- PLO 6: Mampu menganalisis dan menyelesaikan permasalahan jaringan dan keamanannya.
- Indikator-6-3: Mahasiswa mampu menyelesaikan permasalahan yang terjadi pada jaringan dengan solusi yang tepat.
- CPMK-TIO6026-1: Mahasiswa mampu merancang dan mengimplementasikan solusi untuk mengatasi permasalahan komunikasi data dalam jaringan melalui teknik pemrograman socket tingkat lanjut serta integrasi layanan asynchronous messaging dan arsitektur microservices.

Tujuan tugas:
Merancang dan mengimplementasikan komunikasi data antarlayanan berbasis microservices untuk mengatasi tight coupling dan meningkatkan ketersediaan layanan.

Susunan laporan wajib:
1. Halaman Judul
- Judul
- Mata kuliah
- Dosen
- Semester
- Nama dan NIM 5 anggota

2. BAB 1 Pendahuluan
- Latar belakang
- Rumusan masalah
- Tujuan

3. BAB 2 Tinjauan Pustaka
- Konsep microservices
- Konsep gRPC
- Konsep message queue (RabbitMQ)
- Hubungan konsep dengan studi kasus rumah sakit

4. BAB 3 Analisis dan Perancangan
- 3.1 Analisis kebutuhan sistem
- 3.2 Deskripsi komponen (Frontend, Service A, Service B)
- 3.3 Pemilihan dan Justifikasi Teknologi
  - 3.3.1 Teknologi yang dipilih
  - 3.3.2 Alasan mendalam pemilihan (terutama gRPC dan RabbitMQ)
- 3.4 Arsitektur sistem berbasis teknologi terpilih
  - Jelaskan diagram arsitektur
  - Jelaskan alur data langkah demi langkah
  - Tegaskan database isolation dan contract-first

5. BAB 4 Teknik Deployment (konsep)
- Docker dan Docker Compose
- Alur build dan run
- Topologi container dan network
- Cara uji singkat endpoint utama

6. BAB 5 Bukti Penggunaan AI
- Platform AI yang digunakan (Vibe Code / Copilot Chat)
- Bukti prompt yang digunakan
- Paket/library yang digunakan di project
- Penjelasan bagian mana yang dibantu AI dan validasi manual oleh mahasiswa

7. Penutup
- Kesimpulan
- Saran pengembangan

Lampiran yang harus dibuat dalam laporan:
- Lampiran A: Potongan file proto (contract-first)
- Lampiran B: Potongan konfigurasi RabbitMQ/consumer-producer
- Lampiran C: Potongan docker-compose
- Lampiran D: Screenshot alur demo (placeholder jika belum ada)

Aturan penulisan:
- Gunakan heading rapi per BAB.
- Gunakan nomor subbab konsisten.
- Gunakan tabel jika perlu (misal tabel teknologi dan alasan).
- Panjang isi minimal cukup untuk laporan tugas kampus (bukan ringkasan 1-2 halaman).
- Pastikan isi sinkron dengan implementasi microservices yang sudah ada.

Output yang saya minta dari kamu:
1. File Word .docx lengkap.
2. Jika belum bisa generate .docx langsung, buat markdown lengkap yang siap dikonversi ke Word tanpa ubah isi.
3. Sertakan daftar isi otomatis (atau format heading yang siap auto-TOC di Word).
4. Beri placeholder [ISI NAMA/NIM] pada data anggota yang belum diisi.
