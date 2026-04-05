# LAPORAN TUGAS
# IMPLEMENTASI KOMUNIKASI MICROSERVICES

---

**Mata Kuliah:** Jaringan Komputer Terapan
**Dosen Pengampu:** [ISI NAMA DOSEN]
**Semester:** Genap 2025/2026
**Program Studi:** [ISI PRODI]
**Institusi:** [ISI NAMA INSTITUSI]

---

## Anggota Kelompok

| No | Nama | NIM |
|----|------|-----|
| 1  | [ISI NAMA/NIM] | [ISI NIM] |
| 2  | [ISI NAMA/NIM] | [ISI NIM] |
| 3  | [ISI NAMA/NIM] | [ISI NIM] |
| 4  | [ISI NAMA/NIM] | [ISI NIM] |
| 5  | [ISI NAMA/NIM] | [ISI NIM] |

---

## Capaian Pembelajaran

- **PLO 6:** Mampu menganalisis dan menyelesaikan permasalahan jaringan dan keamanannya.
- **Indikator-6-3:** Mahasiswa mampu menyelesaikan permasalahan yang terjadi pada jaringan dengan solusi yang tepat.
- **CPMK-TIO6026-1:** Mahasiswa mampu merancang dan mengimplementasikan solusi untuk mengatasi permasalahan komunikasi data dalam jaringan melalui teknik pemrograman socket tingkat lanjut serta integrasi layanan asynchronous messaging dan arsitektur microservices.

---

## Daftar Isi

1. [BAB 1 — Pendahuluan](#bab-1-pendahuluan)
   - 1.1 Latar Belakang
   - 1.2 Rumusan Masalah
   - 1.3 Tujuan
2. [BAB 2 — Tinjauan Pustaka](#bab-2-tinjauan-pustaka)
   - 2.1 Arsitektur Microservices
   - 2.2 gRPC (Google Remote Procedure Call)
   - 2.3 Message Queue dan RabbitMQ
   - 2.4 Relevansi Konsep pada Studi Kasus Rumah Sakit
3. [BAB 3 — Analisis dan Perancangan](#bab-3-analisis-dan-perancangan)
   - 3.1 Analisis Kebutuhan Sistem
   - 3.2 Deskripsi Komponen
   - 3.3 Pemilihan dan Justifikasi Teknologi
   - 3.4 Arsitektur Sistem
4. [BAB 4 — Teknik Deployment](#bab-4-teknik-deployment)
   - 4.1 Docker dan Docker Compose
   - 4.2 Alur Build dan Run
   - 4.3 Topologi Container dan Network
   - 4.4 Pengujian Endpoint
5. [BAB 5 — Bukti Penggunaan AI](#bab-5-bukti-penggunaan-ai)
   - 5.1 Platform AI yang Digunakan
   - 5.2 Prompt yang Digunakan
   - 5.3 Library yang Digunakan
   - 5.4 Bagian yang Dibantu AI dan Validasi Manual
6. [Penutup](#penutup)
   - 6.1 Kesimpulan
   - 6.2 Saran Pengembangan
7. [Lampiran](#lampiran)

---

# BAB 1 PENDAHULUAN

## 1.1 Latar Belakang

Perkembangan sistem informasi di bidang kesehatan menuntut adanya infrastruktur yang andal, skalabel, dan mudah dikembangkan. Sistem informasi rumah sakit yang dibangun secara tradisional cenderung bersifat monolitik — seluruh fungsi seperti pendaftaran pasien, rekam medis, dan penagihan disatukan dalam satu aplikasi besar. Pendekatan ini memunculkan permasalahan yang dikenal sebagai *tight coupling*, yaitu kondisi di mana komponen-komponen sistem saling bergantung secara ketat sehingga perubahan pada satu bagian dapat berdampak pada seluruh sistem.

Selain itu, sistem monolitik sulit untuk di-*scale* secara parsial. Misalnya, jika modul pendaftaran pasien mendapat lonjakan permintaan, seluruh aplikasi harus di-*scale up*, bukan hanya modul pendaftaran saja. Hal ini menyebabkan pemborosan sumber daya dan penurunan efisiensi operasional.

Untuk menjawab tantangan tersebut, arsitektur **microservices** hadir sebagai paradigma baru dalam pengembangan perangkat lunak. Setiap fungsi bisnis diimplementasikan sebagai layanan kecil yang mandiri (*loosely coupled*), dapat di-*deploy* secara independen, dan berkomunikasi melalui antarmuka yang terdefinisi dengan baik. Komunikasi antar layanan dalam arsitektur microservices umumnya menggunakan dua pendekatan: komunikasi **sinkron** (permintaan langsung dan menunggu respons) serta komunikasi **asinkron** (pengiriman pesan tanpa menunggu).

Proyek ini mengimplementasikan sistem informasi rumah sakit sederhana bernama **MediSync** yang terdiri dari dua layanan utama: **Service A (Pendaftaran Pasien)** dan **Service B (Rekam Medis)**, dengan komunikasi sinkron menggunakan **gRPC** dan komunikasi asinkron menggunakan **RabbitMQ**. Implementasi ini secara langsung menunjukkan bagaimana arsitektur microservices dapat memecahkan permasalahan *tight coupling* dan meningkatkan ketersediaan layanan dalam konteks sistem kesehatan.

## 1.2 Rumusan Masalah

Berdasarkan latar belakang di atas, rumusan masalah dalam tugas ini adalah:

1. Bagaimana merancang arsitektur microservices yang memisahkan fungsi pendaftaran pasien dan rekam medis secara mandiri dengan database yang terisolasi?
2. Bagaimana mengimplementasikan komunikasi sinkron antar layanan menggunakan gRPC untuk validasi data secara real-time?
3. Bagaimana mengimplementasikan komunikasi asinkron menggunakan RabbitMQ agar Service B dapat menerima notifikasi dari Service A tanpa menimbulkan ketergantungan langsung?
4. Bagaimana men-*deploy* seluruh sistem secara terintegrasi menggunakan Docker Compose sehingga mudah dijalankan dan diuji?

## 1.3 Tujuan

Tujuan dari tugas ini adalah:

1. Merancang dan mengimplementasikan arsitektur microservices untuk sistem informasi rumah sakit dengan pemisahan layanan yang jelas.
2. Mengimplementasikan komunikasi data sinkron berbasis gRPC antara Service A dan Service B.
3. Mengimplementasikan komunikasi data asinkron berbasis RabbitMQ menggunakan pola *event-driven*.
4. Memastikan isolasi database antar layanan sebagai prinsip utama microservices.
5. Men-*deploy* seluruh sistem menggunakan Docker Compose agar dapat berjalan secara konsisten di berbagai lingkungan.

---

# BAB 2 TINJAUAN PUSTAKA

## 2.1 Arsitektur Microservices

Arsitektur microservices adalah pendekatan pengembangan perangkat lunak di mana aplikasi dibangun sebagai kumpulan layanan kecil yang dapat di-*deploy* secara independen. Setiap layanan menjalankan proses tersendiri, memiliki database-nya sendiri, dan berkomunikasi melalui mekanisme yang ringan — biasanya HTTP API atau message queue.

Prinsip-prinsip utama arsitektur microservices antara lain:

- **Single Responsibility:** Setiap layanan bertanggung jawab atas satu domain bisnis.
- **Loose Coupling:** Layanan tidak saling bergantung secara langsung; perubahan pada satu layanan tidak merusak layanan lain.
- **High Cohesion:** Kode yang berkaitan dengan satu fungsi bisnis dikelompokkan dalam satu layanan.
- **Database per Service:** Setiap layanan memiliki dan mengelola datanya sendiri. Tidak ada layanan lain yang boleh mengakses database layanan lain secara langsung.
- **Decentralized Data Management:** Tidak ada satu database terpusat untuk seluruh sistem.

Berbeda dengan arsitektur monolitik, microservices memungkinkan tim yang berbeda untuk mengembangkan, menguji, dan men-*deploy* layanan secara independen. Ini meningkatkan kecepatan pengembangan dan ketahanan sistem — jika satu layanan mengalami gangguan, layanan lainnya tetap bisa berjalan.

## 2.2 gRPC (Google Remote Procedure Call)

gRPC adalah framework *Remote Procedure Call* (RPC) modern yang dikembangkan oleh Google. RPC memungkinkan sebuah program untuk memanggil prosedur/fungsi yang berjalan di komputer atau proses lain seolah-olah fungsi tersebut berjalan secara lokal. gRPC menggunakan **HTTP/2** sebagai transport protocol dan **Protocol Buffers (protobuf)** sebagai mekanisme serialisasi data.

Karakteristik utama gRPC:

- **Contract-First:** Antarmuka layanan didefinisikan terlebih dahulu dalam file `.proto` sebelum implementasi kode. Ini memastikan konsistensi antara client dan server.
- **Efisiensi Tinggi:** Protocol Buffers menghasilkan payload yang jauh lebih kecil dibandingkan JSON karena menggunakan format biner.
- **HTTP/2:** Mendukung multiplexing (banyak request dalam satu koneksi), header compression, dan server push.
- **Strongly Typed:** Kontrak antar layanan terdefinisi secara ketat, mengurangi risiko kesalahan tipe data.
- **Multi-bahasa:** gRPC mendukung hampir semua bahasa pemrograman populer (Go, Python, Java, C++, dll).

Dalam proyek MediSync, gRPC digunakan untuk komunikasi **sinkron** antara Service A dan Service B — Service A memanggil fungsi `CheckPatientRecord` di Service B secara langsung dan menunggu respons sebelum melanjutkan proses pendaftaran.

## 2.3 Message Queue dan RabbitMQ

Message Queue adalah pola komunikasi asinkron di mana pengirim (*producer*) menempatkan pesan ke dalam antrian (*queue*), dan penerima (*consumer*) mengambil dan memproses pesan tersebut pada waktu yang berbeda. Pola ini memungkinkan decoupling antara producer dan consumer — producer tidak perlu menunggu consumer selesai memproses.

**RabbitMQ** adalah salah satu message broker paling populer yang mengimplementasikan protokol **AMQP (Advanced Message Queuing Protocol)**. Komponen utama RabbitMQ:

- **Producer:** Aplikasi yang mengirim pesan.
- **Exchange:** Menerima pesan dari producer dan mendistribusikannya ke queue berdasarkan *routing key* dan tipe exchange.
- **Queue:** Tempat penyimpanan pesan sebelum dikonsumsi.
- **Consumer:** Aplikasi yang menerima dan memproses pesan dari queue.
- **Binding:** Aturan yang menghubungkan exchange ke queue.

Tipe exchange yang digunakan dalam proyek ini adalah **direct exchange** — pesan dikirim ke queue yang *routing key*-nya persis sama dengan routing key pada pengiriman pesan.

Keunggulan penggunaan RabbitMQ:

- **Decoupling:** Service A tidak perlu tahu apakah Service B sedang berjalan atau tidak saat mengirim event.
- **Reliability:** Pesan dapat di-*persist* agar tidak hilang jika broker restart.
- **Backpressure Handling:** Consumer bisa memproses pesan sesuai kapasitasnya tanpa membebani producer.

## 2.4 Relevansi Konsep dengan Studi Kasus Rumah Sakit

Dalam konteks sistem informasi rumah sakit, pemisahan layanan pendaftaran dan rekam medis menjadi dua microservice yang terpisah mencerminkan realitas operasional rumah sakit yang sesungguhnya:

- **Pendaftaran pasien** adalah proses yang berhadapan langsung dengan pasien — harus cepat dan responsif. Jika terjadi gangguan pada sistem rekam medis, proses pendaftaran tidak boleh ikut terganggu.
- **Rekam medis** membutuhkan data yang akurat dan konsisten — pembuatan rekam medis dapat dilakukan secara asinkron setelah pendaftaran selesai.
- **Validasi real-time via gRPC** diperlukan saat pendaftaran untuk memastikan seorang pasien tidak terdaftar dua kali — ini adalah komunikasi sinkron karena keputusan harus dibuat sebelum menyimpan data.
- **Event-driven via RabbitMQ** digunakan untuk memberitahu Service B bahwa ada pasien baru yang perlu dibuatkan draft rekam medis — ini tidak perlu sinkron karena pembuatan draft tidak memblokir proses pendaftaran.

---

# BAB 3 ANALISIS DAN PERANCANGAN

## 3.1 Analisis Kebutuhan Sistem

### 3.1.1 Kebutuhan Fungsional

| ID | Kebutuhan |
|----|-----------|
| KF-01 | Sistem dapat menerima input data pasien baru melalui antarmuka web |
| KF-02 | Sistem dapat memvalidasi apakah pasien sudah pernah terdaftar sebelum menyimpan data |
| KF-03 | Sistem dapat menyimpan data pasien ke database pendaftaran |
| KF-04 | Sistem dapat mengirimkan notifikasi ke layanan rekam medis saat pasien baru terdaftar |
| KF-05 | Sistem rekam medis dapat membuat draft rekam medis secara otomatis |
| KF-06 | Pengguna dapat melihat daftar pasien yang terdaftar |
| KF-07 | Pengguna dapat mencari rekam medis berdasarkan NIK |

### 3.1.2 Kebutuhan Non-Fungsional

| ID | Kebutuhan |
|----|-----------|
| KNF-01 | Layanan harus dapat berjalan secara independen (fault isolation) |
| KNF-02 | Setiap layanan memiliki database terpisah (database isolation) |
| KNF-03 | Kontrak komunikasi antar layanan harus terdefinisi secara eksplisit (contract-first) |
| KNF-04 | Sistem harus memiliki mekanisme retry saat koneksi database atau broker gagal |
| KNF-05 | Seluruh sistem harus dapat dijalankan dengan satu perintah Docker Compose |

## 3.2 Deskripsi Komponen

### 3.2.1 Frontend (React + Vite)

Frontend merupakan antarmuka pengguna yang diakses melalui browser. Dibangun dengan React 18 dan Vite sebagai build tool. Frontend bertugas:

- Menampilkan formulir pendaftaran pasien baru
- Mengirimkan data pasien ke Service A melalui HTTP POST
- Menampilkan daftar pasien yang sudah terdaftar
- Memberikan feedback visual kepada pengguna (loading state, error message, success message)

Frontend **tidak berkomunikasi langsung** dengan Service B maupun database. Seluruh komunikasi dilakukan melalui Service A.

### 3.2.2 Service A — Pendaftaran (Go + Gin)

Service A adalah layanan inti pendaftaran pasien. Berjalan di port **4001** dan merupakan satu-satunya layanan yang dapat diakses oleh frontend. Tanggung jawab Service A:

- Menerima dan memvalidasi data pasien dari frontend
- Memanggil Service B via gRPC untuk mengecek apakah NIK sudah terdaftar (komunikasi sinkron)
- Menyimpan data pasien ke `db_pendaftaran` jika belum terdaftar
- Mempublikasikan event `patient.registered` ke RabbitMQ (komunikasi asinkron)
- Menyediakan endpoint GET untuk membaca daftar pasien

**Database:** `db_pendaftaran` dengan tabel `patients`

**Endpoints:**
- `POST /api/patients` — mendaftarkan pasien baru
- `GET /api/patients` — mengambil semua data pasien
- `GET /health` — health check

### 3.2.3 Service B — Rekam Medis (Go + Gin + gRPC Server)

Service B adalah layanan pengelola rekam medis. Berjalan di port **4002** (HTTP) dan **50052** (gRPC). Service B bertindak sebagai gRPC server sekaligus consumer RabbitMQ. Tanggung jawab Service B:

- Melayani panggilan gRPC `CheckPatientRecord` dari Service A
- Mengonsumsi event `patient.registered` dari RabbitMQ
- Membuat draft rekam medis di `db_rekam_medis` saat menerima event
- Menyediakan endpoint GET untuk membaca rekam medis

**Database:** `db_rekam_medis` dengan tabel `medical_records`

**Endpoints:**
- `GET /api/records` — mengambil semua rekam medis
- `GET /api/records/:nik` — mengambil rekam medis berdasarkan NIK
- `GET /health` — health check

## 3.3 Pemilihan dan Justifikasi Teknologi

### 3.3.1 Teknologi yang Dipilih

| Komponen | Teknologi | Versi |
|----------|-----------|-------|
| Backend Services | Go (Golang) | 1.21 |
| HTTP Framework | Gin | v1.9.1 |
| RPC Framework | gRPC + Protocol Buffers | v1.62.0 |
| Message Broker | RabbitMQ | 3.12 |
| Database | PostgreSQL | 15 |
| Database Driver | lib/pq | v1.10.9 |
| AMQP Client | amqp091-go | v1.9.0 |
| Frontend | React + Vite | 18 + 5 |
| HTTP Client (FE) | Axios | v1.6.7 |
| Containerization | Docker + Docker Compose | - |

### 3.3.2 Alasan Mendalam Pemilihan Teknologi

**Go (Golang) untuk Backend:**

Go dipilih karena karakteristiknya yang sangat sesuai untuk membangun microservices:
- **Performa tinggi:** Go dikompilasi menjadi binary native, menjadikannya jauh lebih efisien dari bahasa interpreted seperti Python atau Node.js.
- **Concurrency model:** Goroutine dan channel milik Go memudahkan penanganan banyak request secara bersamaan tanpa overhead thread yang besar.
- **Binary tunggal:** Hasil kompilasi Go adalah satu binary yang dapat langsung dijalankan di Alpine Linux tanpa dependency runtime, menjadikan Docker image sangat kecil dan portabel.
- **Dukungan gRPC kelas satu:** Google mengembangkan gRPC dengan dukungan Go yang sangat matang.

**gRPC untuk Komunikasi Sinkron:**

Dibandingkan REST/HTTP biasa, gRPC dipilih karena:
- **Contract-first:** File `.proto` mendefinisikan antarmuka layanan sebelum implementasi. Ini memaksa kedua layanan untuk menyepakati kontrak terlebih dahulu, mengurangi risiko *breaking changes*.
- **Efisiensi serialisasi:** Protocol Buffers menghasilkan payload biner yang 3-10x lebih kecil dan lebih cepat diparse dibandingkan JSON.
- **Type safety:** Compiler akan menolak kode yang tidak sesuai dengan kontrak proto, menangkap bug di waktu kompilasi bukan runtime.
- **Kesesuaian use case:** Validasi NIK memerlukan latensi rendah dan kepastian tipe data — cocok untuk gRPC.

**RabbitMQ untuk Komunikasi Asinkron:**

Dibandingkan HTTP callback atau polling, RabbitMQ dipilih karena:
- **Decoupling total:** Service A tidak perlu tahu apakah Service B sedang up atau down saat mengirim event. RabbitMQ menjamin pesan tersimpan di queue sampai dikonsumsi.
- **Durability:** Dengan konfigurasi `durable=true` pada queue dan `DeliveryMode=Persistent` pada pesan, data tidak hilang meskipun RabbitMQ restart.
- **Pola yang tepat:** Pembuatan draft rekam medis adalah side-effect dari pendaftaran, bukan bagian dari alur utama. Ini adalah use case ideal untuk event-driven async.
- **Management UI:** RabbitMQ menyediakan antarmuka web bawaan di port 15672 yang sangat membantu untuk monitoring dan debugging.

**PostgreSQL dengan Database Terpisah:**

- **Database isolation adalah prinsip wajib microservices.** Setiap service hanya boleh mengakses database-nya sendiri. Ini memastikan bahwa Service A dan Service B dapat di-*develop*, di-*deploy*, dan di-*scale* secara benar-benar independen.
- PostgreSQL dipilih karena mendukung UUID natively via ekstensi `pgcrypto`, memiliki ACID compliance, dan merupakan database relasional yang paling battle-tested di dunia open source.

## 3.4 Arsitektur Sistem Berbasis Teknologi Terpilih

### 3.4.1 Diagram Arsitektur

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Docker Network: medisync-net                 │
│                                                                      │
│   ┌──────────────┐    HTTP/REST    ┌─────────────────────────────┐  │
│   │   Frontend   │◄───────────────►│       Service A             │  │
│   │  React+Vite  │   POST/GET      │  (Pendaftaran - Port 4001)  │  │
│   │  Port: 3000  │                 └──────────┬──────────────────┘  │
│   └──────────────┘                            │                      │
│                                    ┌──────────┤                      │
│                                    │          │                      │
│                              gRPC  │    MQ    │                      │
│                           (Sync)   │  (Async) │                      │
│                                    ▼          ▼                      │
│                         ┌──────────────┐  ┌──────────┐              │
│                         │  Service B   │  │RabbitMQ  │              │
│                         │ (Rekam Medis │◄─┤ Port:    │              │
│                         │  Port: 4002/ │  │ 5672/    │              │
│                         │       50052) │  │ 15672 UI │              │
│                         └──────┬───────┘  └──────────┘              │
│                                │                                     │
│              ┌─────────────────┴──────────────────┐                 │
│              │          PostgreSQL (Port 5432)     │                 │
│              │  ┌─────────────────┐ ┌────────────┐ │                │
│              │  │ db_pendaftaran  │ │db_rekam_   │ │                │
│              │  │  (Service A DB) │ │medis       │ │                │
│              │  └─────────────────┘ │(Service B) │ │                │
│              │                      └────────────┘ │                │
│              └────────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.4.2 Alur Data Langkah demi Langkah

Berikut adalah alur lengkap dari momen pengguna mengisi formulir hingga draft rekam medis terbentuk:

**Langkah 1 — Input dari Frontend:**
Pengguna mengisi formulir dengan data: Nama Lengkap, NIK (16 digit), Tanggal Lahir, dan Nomor Telepon. Frontend melakukan validasi sisi klien (NIK harus 16 digit angka, nama tidak boleh kosong). Jika valid, frontend mengirim HTTP POST ke `http://localhost:4001/api/patients` dengan payload JSON.

**Langkah 2 — Validasi gRPC (Sinkron):**
Service A menerima request dan melakukan validasi server-side. Kemudian Service A membuka koneksi gRPC ke Service B di `service-b:50052` dan memanggil `CheckPatientRecord(nik)`. Service A **menunggu** respons dari Service B sebelum melanjutkan. Service B melakukan query ke `db_rekam_medis` untuk mencari rekam medis dengan NIK tersebut. Jika ditemukan, Service B mengembalikan `has_record=true`; jika tidak, `has_record=false`.

**Langkah 3 — Cek Duplikasi:**
Jika Service B mengembalikan `has_record=true`, Service A langsung mengembalikan HTTP 409 Conflict ke frontend dengan pesan "Pasien dengan NIK ini sudah pernah terdaftar." Proses berhenti di sini.

**Langkah 4 — Simpan ke Database Pendaftaran:**
Jika NIK belum terdaftar, Service A menjalankan query INSERT ke `db_pendaftaran`, menyimpan data pasien dan mendapatkan UUID yang di-*generate* oleh PostgreSQL sebagai `patient_id`.

**Langkah 5 — Publish Event ke RabbitMQ (Asinkron):**
Service A mempublikasikan event `patient.registered` ke exchange `hospital` di RabbitMQ dengan routing key `patient.registered`. Payload event berisi: `patient_id`, `name`, `nik`, `tanggal_lahir`, `no_telepon`, dan `timestamp`. Proses publish dilakukan di goroutine terpisah agar tidak memblokir response ke frontend.

**Langkah 6 — Response ke Frontend:**
Service A langsung mengembalikan HTTP 201 Created ke frontend dengan data pasien yang baru didaftarkan. Frontend menampilkan pesan sukses dan memperbarui daftar pasien.

**Langkah 7 — Consume Event di Service B (Asinkron):**
Di sisi Service B, consumer RabbitMQ yang berjalan di goroutine tersendiri menerima event dari queue `patient.queue`. Consumer melakukan parsing JSON payload dan menjalankan INSERT ke `db_rekam_medis` untuk membuat draft rekam medis. Jika INSERT gagal, pesan di-*nack* (negative acknowledgement) dan di-*requeue* untuk dicoba lagi. Jika berhasil, pesan di-*ack* (positive acknowledgement) sehingga dihapus dari queue.

### 3.4.3 Prinsip Database Isolation

Salah satu prinsip terpenting dalam arsitektur microservices adalah **"database per service"**. Dalam implementasi MediSync:

- **Service A hanya mengakses `db_pendaftaran`** — koneksi database di Service A dikonfigurasi dengan DSN `postgres://admin:secret123@postgres:5432/db_pendaftaran`. Tidak ada query yang menyentuh `db_rekam_medis`.
- **Service B hanya mengakses `db_rekam_medis`** — koneksi database di Service B dikonfigurasi dengan DSN `postgres://admin:secret123@postgres:5432/db_rekam_medis`. Tidak ada query yang menyentuh `db_pendaftaran`.
- **Komunikasi antar domain data** dilakukan melalui mekanisme komunikasi resmi (gRPC atau RabbitMQ), bukan melalui *direct database join*.

### 3.4.4 Prinsip Contract-First

File `proto/medical_record.proto` mendefinisikan kontrak gRPC:

```protobuf
service MedicalRecordService {
  rpc CheckPatientRecord (PatientRequest) returns (RecordResponse);
}

message PatientRequest {
  string nik = 1;
}

message RecordResponse {
  bool   has_record = 1;
  string record_id  = 2;
  string message    = 3;
}
```

File `.pb.go` yang dihasilkan dari proto ini di-*copy* ke direktori `internal/proto` di kedua service. Ini memastikan bahwa Service A (client) dan Service B (server) selalu menggunakan kontrak yang sama. Perubahan pada kontrak harus dilakukan di file `.proto` terlebih dahulu, kemudian di-*regenerate* dan di-*update* di kedua service.

---

# BAB 4 TEKNIK DEPLOYMENT

## 4.1 Docker dan Docker Compose

**Docker** adalah platform containerization yang memungkinkan aplikasi dikemas beserta semua dependensinya ke dalam sebuah *container* yang terisolasi. Container berjalan konsisten di mana pun — laptop pengembang, server staging, maupun server produksi — karena membawa environment-nya sendiri.

**Docker Compose** adalah tool untuk mendefinisikan dan menjalankan aplikasi multi-container menggunakan satu file konfigurasi `docker-compose.yml`. Dengan satu perintah `docker compose up --build`, seluruh stack (frontend, service-a, service-b, postgres, rabbitmq) dapat dibangun dan dijalankan secara bersamaan dengan urutan dependensi yang benar.

Setiap service menggunakan **multi-stage build** di Dockerfile:
- **Stage 1 (builder):** Menggunakan image `golang:1.21-alpine` yang besar untuk mengkompilasi source code menjadi binary.
- **Stage 2 (runner):** Hanya menyalin binary hasil kompilasi ke image `alpine:3.19` yang sangat kecil (~5MB). Hasilnya adalah image yang ringan dan aman karena tidak mengandung compiler atau source code.

## 4.2 Alur Build dan Run

Untuk menjalankan seluruh sistem:

```bash
# Clone atau masuk ke direktori project
cd MediSync

# Bangun dan jalankan semua service sekaligus
docker compose up --build

# Untuk menjalankan di background
docker compose up --build -d

# Untuk melihat log semua service
docker compose logs -f

# Untuk melihat log service tertentu
docker compose logs -f service-a

# Untuk menghentikan semua service
docker compose down

# Untuk menghentikan dan menghapus volume (reset data)
docker compose down -v
```

Urutan startup yang dikonfigurasi di `docker-compose.yml`:
1. **postgres** — startup pertama; service lain menunggu healthcheck `pg_isready` sebelum lanjut
2. **rabbitmq** — startup bersamaan dengan postgres; service lain menunggu healthcheck `rabbitmq-diagnostics ping`
3. **service-b** — startup setelah postgres dan rabbitmq healthy; service-a menunggu service-b started
4. **service-a** — startup setelah postgres, rabbitmq healthy, dan service-b started
5. **frontend** — startup terakhir setelah service-a

Selain dependensi startup, semua service Go juga memiliki **retry loop internal** — jika koneksi ke database atau RabbitMQ gagal, service akan mencoba kembali hingga 10 kali dengan interval 3-4 detik sebelum menyerah. Ini memberikan toleransi terhadap delay startup container.

## 4.3 Topologi Container dan Network

Semua container bergabung dalam satu Docker network bernama `medisync-net` dengan driver `bridge`. Dalam network ini, container dapat saling berkomunikasi menggunakan nama service sebagai hostname:

| Service | Hostname (dalam network) | Port Internal | Port Host |
|---------|--------------------------|---------------|-----------|
| postgres | `postgres` | 5432 | 5432 |
| rabbitmq | `rabbitmq` | 5672, 15672 | 5672, 15672 |
| service-b | `service-b` | 4002, 50052 | 4002, 50052 |
| service-a | `service-a` | 4001 | 4001 |
| frontend | `frontend` | 80 | 3000 |

Variabel lingkungan yang dikonfigurasi untuk komunikasi antar service:
- `DB_URL` di Service A: `postgres://admin:secret123@postgres:5432/db_pendaftaran`
- `DB_URL` di Service B: `postgres://admin:secret123@postgres:5432/db_rekam_medis`
- `RABBITMQ_URL` di kedua service: `amqp://guest:guest@rabbitmq:5672/`
- `GRPC_SERVICE_B` di Service A: `service-b:50052`

## 4.4 Pengujian Endpoint

Setelah `docker compose up --build` berhasil, endpoint dapat diuji sebagai berikut:

**Uji Health Check:**
```bash
curl http://localhost:4001/health
# Expected: {"service":"service-a","status":"ok"}

curl http://localhost:4002/health
# Expected: {"service":"service-b","status":"ok"}
```

**Uji Pendaftaran Pasien Baru:**
```bash
curl -X POST http://localhost:4001/api/patients \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Budi Santoso",
    "nik": "3201234567890001",
    "tanggal_lahir": "1990-05-15",
    "no_telepon": "08123456789"
  }'

# Expected: HTTP 201
# {
#   "success": true,
#   "message": "Pasien berhasil didaftarkan.",
#   "data": { "patient_id": "...", "name": "Budi Santoso", ... }
# }
```

**Uji Duplikasi (NIK yang sama):**
```bash
# Kirim request yang sama dua kali — request kedua harus ditolak
curl -X POST http://localhost:4001/api/patients \
  -H "Content-Type: application/json" \
  -d '{ "name": "Budi Santoso", "nik": "3201234567890001", ... }'

# Expected: HTTP 409
# { "success": false, "message": "Pasien dengan NIK ini sudah pernah terdaftar..." }
```

**Uji Daftar Pasien:**
```bash
curl http://localhost:4001/api/patients
# Expected: HTTP 200 dengan array data pasien
```

**Uji Rekam Medis (beberapa detik setelah pendaftaran):**
```bash
curl http://localhost:4002/api/records/3201234567890001
# Expected: HTTP 200 dengan data draft rekam medis yang dibuat otomatis via RabbitMQ
```

**Akses RabbitMQ Management UI:**
Buka browser ke `http://localhost:15672` dengan username: `guest`, password: `guest`. Di sini dapat dilihat antrian, exchange, dan aktivitas message yang sedang berjalan.

---

# BAB 5 BUKTI PENGGUNAAN AI

## 5.1 Platform AI yang Digunakan

Dalam pengerjaan proyek MediSync, digunakan bantuan AI sebagai alat bantu pemrograman (*vibe coding*). Platform yang digunakan:

- **Claude Code (Anthropic)** — Digunakan untuk audit kode, perbaikan bug, dan pembuatan laporan.
- **GitHub Copilot / AI Chat** — Digunakan untuk autocomplete kode dan saran implementasi awal.

## 5.2 Prompt yang Digunakan

Berikut adalah contoh prompt utama yang digunakan selama pengerjaan proyek:

**Prompt 1 — Implementasi Source Code:**
> *"Tolong audit dan rapikan seluruh source code agar sinkron dengan requirement tugas dan siap demo tanpa error. Requirement wajib: (1) Arsitektur Microservices dengan Frontend, Service A, Service B; (2) gRPC sinkron antara Service A dan Service B; (3) RabbitMQ asinkron untuk event patient.registered; (4) Database isolation; (5) Contract-first dengan proto file..."*

**Prompt 2 — Generate Laporan:**
> *"Tolong buatkan dokumen laporan lengkap dalam format Word (.docx) yang siap dikumpulkan. Bahasa: Indonesia mahasiswa, natural, jelas. Judul tugas: Implementasi Komunikasi Microservices..."*

## 5.3 Paket/Library yang Digunakan

**Service A & Service B (Go):**

| Library | Versi | Fungsi |
|---------|-------|--------|
| `github.com/gin-gonic/gin` | v1.9.1 | HTTP framework untuk REST API |
| `github.com/gin-contrib/cors` | v1.5.0 | Middleware CORS untuk Gin |
| `google.golang.org/grpc` | v1.62.0 | Framework gRPC |
| `google.golang.org/protobuf` | v1.33.0 | Runtime Protocol Buffers |
| `github.com/lib/pq` | v1.10.9 | Driver PostgreSQL untuk Go |
| `github.com/rabbitmq/amqp091-go` | v1.9.0 | Client AMQP untuk RabbitMQ |
| `github.com/google/uuid` | v1.6.0 | Utilitas UUID |

**Frontend (Node.js/React):**

| Library | Versi | Fungsi |
|---------|-------|--------|
| `react` | v18.2.0 | Library UI utama |
| `react-dom` | v18.2.0 | React untuk browser DOM |
| `axios` | v1.6.7 | HTTP client untuk request ke Service A |
| `vite` | v5.1.3 | Build tool dan dev server |
| `@vitejs/plugin-react` | v4.2.1 | Plugin Vite untuk JSX/React |

## 5.4 Bagian yang Dibantu AI dan Validasi Manual

| Bagian | Dibantu AI | Validasi Manual |
|--------|-----------|-----------------|
| Struktur folder project | Ya — AI menyarankan struktur direktori | Disesuaikan dengan modul Go yang digunakan |
| File `proto/medical_record.proto` | Sebagian — desain message dan service | Diverifikasi kesesuaian dengan alur bisnis |
| File `.pb.go` (generated) | Ya — di-generate dari proto | Dicek apakah sesuai dengan proto file |
| `service-a/internal/handler/patient.go` | Sebagian — kerangka handler | Diuji alur gRPC → DB → MQ secara manual |
| `service-a/internal/grpc/client.go` | Ya — boilerplate gRPC client | Diverifikasi target dan timeout yang wajar |
| `service-a/internal/mq/producer.go` | Ya — konfigurasi exchange & publish | Diverifikasi routing key dan durability |
| `service-b/internal/grpc/server.go` | Ya — implementasi gRPC server | Diuji apakah query DB benar |
| `service-b/internal/mq/consumer.go` | Ya — logika consume dan ack/nack | Diverifikasi logika ON CONFLICT dan requeue |
| `docker-compose.yml` | Ya — konfigurasi healthcheck | Diverifikasi urutan depends_on dan env vars |
| Frontend komponen React | Ya — kerangka form dan tabel | Diuji validasi NIK, error handling, dan tampilan |

Seluruh kode yang dibantu AI tetap melalui proses review dan pengujian manual. Beberapa bug ditemukan saat pengujian dan diperbaiki secara manual, antara lain:
- Retry logic database yang tidak mendeteksi ping error dengan benar
- Error handling endpoint `GetRecordByNIK` yang tidak membedakan "tidak ditemukan" dari "error database"
- Dockerfile yang tidak menangani ketiadaan `go.sum` dengan graceful

---

# PENUTUP

## 6.1 Kesimpulan

Melalui implementasi proyek MediSync, dapat disimpulkan bahwa:

1. **Arsitektur microservices berhasil diterapkan** dalam konteks sistem informasi rumah sakit dengan pemisahan yang jelas antara Service A (Pendaftaran) dan Service B (Rekam Medis). Setiap service memiliki database, codebase, dan container yang sepenuhnya independen.

2. **gRPC terbukti efektif untuk komunikasi sinkron** antar layanan. Pendekatan contract-first dengan file `.proto` memastikan konsistensi antarmuka, sementara Protocol Buffers memberikan efisiensi serialisasi yang lebih baik dibandingkan JSON biasa. Validasi NIK real-time berjalan dengan latensi rendah dan type safety yang terjamin.

3. **RabbitMQ berhasil mengimplementasikan pola event-driven** untuk komunikasi asinkron. Service A dapat menyelesaikan proses pendaftaran dan memberikan respons ke pengguna tanpa harus menunggu Service B selesai membuat rekam medis. Ini meningkatkan responsivitas sistem secara keseluruhan.

4. **Database isolation berhasil dipertahankan** — tidak ada satu pun query lintas database dalam seluruh codebase. Komunikasi antar domain dilakukan sepenuhnya melalui gRPC dan RabbitMQ.

5. **Docker Compose menyederhanakan deployment** seluruh sistem yang terdiri dari 5 container (frontend, service-a, service-b, postgres, rabbitmq) menjadi satu perintah. Healthcheck dan depends_on memastikan urutan startup yang benar.

## 6.2 Saran Pengembangan

Beberapa area yang dapat dikembangkan lebih lanjut:

1. **API Gateway:** Menambahkan reverse proxy (misal: Nginx atau Traefik) sebagai single entry point untuk seluruh layanan, sehingga frontend tidak perlu tahu alamat masing-masing service.

2. **Autentikasi dan Otorisasi:** Mengimplementasikan JWT atau OAuth2 untuk mengamankan endpoint API, terutama untuk data medis yang sensitif.

3. **Circuit Breaker:** Menambahkan pola circuit breaker pada koneksi gRPC di Service A agar sistem tetap responsif meskipun Service B tidak tersedia dalam jangka waktu tertentu.

4. **Observability:** Menambahkan distributed tracing (Jaeger/Zipkin), metrics (Prometheus + Grafana), dan centralized logging (ELK Stack) untuk memudahkan monitoring dan debugging di lingkungan produksi.

5. **Service Discovery:** Mengintegrasikan service discovery (Consul atau Kubernetes DNS) agar service tidak bergantung pada konfigurasi hostname statis.

6. **gRPC TLS:** Menambahkan Transport Layer Security (TLS) pada koneksi gRPC untuk keamanan data saat transit.

7. **Dead Letter Queue:** Mengkonfigurasi Dead Letter Exchange (DLX) di RabbitMQ untuk menangani pesan yang gagal diproses berulang kali, sehingga tidak masuk ke loop requeue tanpa batas.

---

# LAMPIRAN

## Lampiran A — File Proto (Contract-First)

File: `proto/medical_record.proto`

```protobuf
syntax = "proto3";

package medicalrecord;

option go_package = "./proto";

// MedicalRecordService mendefinisikan kontrak gRPC antara Service A dan Service B.
// Service A bertindak sebagai Client, Service B sebagai Server.
service MedicalRecordService {
  // CheckPatientRecord: cek apakah pasien sudah memiliki rekam medis di Service B
  // Dipanggil secara SYNCHRONOUS oleh Service A sebelum mendaftarkan pasien
  rpc CheckPatientRecord (PatientRequest) returns (RecordResponse);
}

message PatientRequest {
  string nik = 1;
}

message RecordResponse {
  bool   has_record = 1;
  string record_id  = 2;
  string message    = 3;
}
```

File `.proto` ini adalah **satu-satunya sumber kebenaran** (single source of truth) untuk kontrak komunikasi gRPC antara Service A dan Service B. Baik client (Service A) maupun server (Service B) menggunakan file Go yang di-*generate* dari proto ini, memastikan tidak ada ketidaksesuaian tipe data.

---

## Lampiran B — Potongan Konfigurasi RabbitMQ Producer dan Consumer

**Producer (Service A) — `service-a/internal/mq/producer.go`:**

```go
const (
    exchangeName = "hospital"
    routingKey   = "patient.registered"
)

func Connect() {
    // ... retry loop 15x dengan interval 4 detik ...
    
    // Deklarasi exchange tipe "direct", durable
    ch.ExchangeDeclare(exchangeName, "direct", true, false, false, false, nil)
}

func PublishPatientRegistered(event PatientEvent) error {
    body, _ := json.Marshal(event)
    
    return ch.PublishWithContext(ctx,
        exchangeName,  // exchange
        routingKey,    // routing key: "patient.registered"
        false, false,
        amqp.Publishing{
            ContentType:  "application/json",
            DeliveryMode: amqp.Persistent,  // pesan tidak hilang saat restart
            Body:         body,
        },
    )
}
```

**Consumer (Service B) — `service-b/internal/mq/consumer.go`:**

```go
func Start() {
    // Deklarasi exchange, queue, dan binding
    ch.ExchangeDeclare(exchangeName, "direct", true, false, false, false, nil)
    
    q, _ := ch.QueueDeclare(
        "patient.queue",  // nama queue
        true,             // durable — queue tidak hilang saat restart
        false, false, false, nil,
    )
    
    ch.QueueBind(q.Name, "patient.registered", exchangeName, false, nil)
    
    msgs, _ := ch.Consume(q.Name, "", false, false, false, false, nil)
    
    for msg := range msgs {
        processEvent(msg)  // proses satu per satu
    }
}

func processEvent(msg amqp.Delivery) {
    var event PatientEvent
    json.Unmarshal(msg.Body, &event)
    
    // Insert draft rekam medis, abaikan jika NIK sudah ada
    db.DB.Exec(`INSERT INTO medical_records (patient_id, name, nik, ...)
                VALUES ($1, $2, $3, ...) ON CONFLICT (nik) DO NOTHING`, ...)
    
    msg.Ack(false)   // konfirmasi berhasil diproses
    // atau msg.Nack(false, true) jika gagal — requeue
}
```

---

## Lampiran C — Potongan Docker Compose

File: `docker-compose.yml`

```yaml
version: "3.9"

networks:
  medisync-net:
    driver: bridge

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret123
      POSTGRES_DB: postgres
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./init-db.sql:/docker-entrypoint-initdb.d/init-db.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin"]
      interval: 10s
      retries: 5

  rabbitmq:
    image: rabbitmq:3.12-management-alpine
    ports:
      - "5672:5672"
      - "15672:15672"
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 15s
      retries: 5

  service-b:
    build: ./service-b
    environment:
      DB_URL: "postgres://admin:secret123@postgres:5432/db_rekam_medis?sslmode=disable"
      RABBITMQ_URL: "amqp://guest:guest@rabbitmq:5672/"
      GRPC_PORT: "50052"
    ports:
      - "4002:4002"
      - "50052:50052"
    depends_on:
      postgres: { condition: service_healthy }
      rabbitmq: { condition: service_healthy }
    restart: on-failure

  service-a:
    build: ./service-a
    environment:
      DB_URL: "postgres://admin:secret123@postgres:5432/db_pendaftaran?sslmode=disable"
      RABBITMQ_URL: "amqp://guest:guest@rabbitmq:5672/"
      GRPC_SERVICE_B: "service-b:50052"
    ports:
      - "4001:4001"
    depends_on:
      postgres: { condition: service_healthy }
      rabbitmq: { condition: service_healthy }
      service-b: { condition: service_started }
    restart: on-failure

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - service-a
```

---

## Lampiran D — Screenshot Alur Demo

*[Screenshot harus diambil saat demo berlangsung dan disisipkan di sini]*

**D.1 — Halaman Utama Frontend**
`[Screenshot: tampilan awal aplikasi MediSync di http://localhost:3000]`

**D.2 — Pengisian Formulir Pendaftaran**
`[Screenshot: form diisi dengan data pasien: nama, NIK 16 digit, tanggal lahir]`

**D.3 — Respons Sukses Pendaftaran**
`[Screenshot: pesan "Pasien berhasil didaftarkan" dengan Patient ID yang ditampilkan]`

**D.4 — Log Service A (gRPC + RabbitMQ)**
`[Screenshot: terminal log Service A menampilkan alur: → Mengecek gRPC → ✓ Simpan DB → ✓ Event dikirim]`

**D.5 — Log Service B (Consumer Event)**
`[Screenshot: terminal log Service B menampilkan: ← Event diterima → ✓ Draft rekam medis dibuat]`

**D.6 — Verifikasi Rekam Medis via API**
`[Screenshot: curl GET /api/records/:nik menampilkan draft rekam medis yang dibuat otomatis]`

**D.7 — RabbitMQ Management UI**
`[Screenshot: http://localhost:15672 menampilkan exchange "hospital" dan queue "patient.queue"]`

**D.8 — Uji Duplikasi NIK**
`[Screenshot: pendaftaran kedua dengan NIK yang sama menghasilkan HTTP 409 Conflict]`

---

*Dokumen ini dibuat untuk keperluan tugas mata kuliah Jaringan Komputer Terapan.*
*MediSync © 2025/2026 — Implementasi Komunikasi Microservices*
