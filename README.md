# MediSync — Implementasi Komunikasi Microservices

> **Tugas Jaringan Komputer Terapan | Semester Genap 2025/2026**
>
> Studi kasus: Sistem Informasi Rumah Sakit berbasis arsitektur **Microservices**
> dengan komunikasi **gRPC (sinkron)** dan **RabbitMQ (asinkron)**.

---

## Capaian Pembelajaran

| Kode | Deskripsi |
|------|-----------|
| PLO 6 | Mampu menganalisis dan menyelesaikan permasalahan jaringan dan keamanannya |
| Indikator-6-3 | Mampu menyelesaikan permasalahan jaringan dengan solusi yang tepat |
| CPMK-TIO6026-1 | Mampu merancang dan mengimplementasikan solusi komunikasi data melalui asynchronous messaging dan arsitektur microservices |

---

## Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────────┐
│                  Docker Network: medisync-net                │
│                                                             │
│  ┌──────────────┐  HTTP/REST  ┌──────────────────────────┐ │
│  │   Frontend   │────────────►│       Service A          │ │
│  │ React + Vite │  POST /api  │  Pendaftaran | Port 4001 │ │
│  │  Port: 3000  │             └──────────┬───────────────┘ │
│  └──────────────┘                        │                  │
│                              ┌───────────┤                  │
│                         gRPC │     MQ    │                  │
│                        (sync)│   (async) │                  │
│                              ▼           ▼                  │
│                   ┌──────────────┐  ┌──────────┐           │
│                   │  Service B   │◄─┤ RabbitMQ │           │
│                   │  Rekam Medis │  │ :5672    │           │
│                   │  :4002/50052 │  │ UI:15672 │           │
│                   └──────┬───────┘  └──────────┘           │
│                          │                                   │
│          ┌───────────────┴──────────────────┐               │
│          │         PostgreSQL :5432          │               │
│          │  ┌──────────────┐ ┌────────────┐ │               │
│          │  │db_pendaftaran│ │db_rekam_   │ │               │
│          │  │ (Service A)  │ │medis (B)   │ │               │
│          │  └──────────────┘ └────────────┘ │               │
│          └──────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Komponen | Teknologi | Port |
|----------|-----------|------|
| Frontend | React 18 + Vite + Axios | 3000 |
| Service A | Go 1.21 + Gin + gRPC Client | 4001 |
| Service B | Go 1.21 + Gin + gRPC Server | 4002 / 50052 |
| Database A | PostgreSQL 15 — `db_pendaftaran` | 5432 |
| Database B | PostgreSQL 15 — `db_rekam_medis` | 5432 |
| Message Broker | RabbitMQ 3.12 | 5672 / 15672 |
| Deployment | Docker Compose | — |

---

## Struktur Repository

```
MediSync/
├── proto/
│   └── medical_record.proto        ← Kontrak gRPC (contract-first)
│
├── service-a/                      ← Service Pendaftaran
│   ├── cmd/main.go
│   ├── internal/
│   │   ├── db/postgres.go          ← Koneksi db_pendaftaran
│   │   ├── grpc/
│   │   │   ├── client.go           ← gRPC client ke Service B
│   │   │   └── codec.go            ← JSON codec workaround untuk .pb.go manual
│   │   ├── handler/patient.go      ← POST /api/patients, GET /api/patients
│   │   ├── mq/producer.go          ← Publish event patient.registered
│   │   └── proto/                  ← Generated stubs dari medical_record.proto
│   ├── go.mod
│   ├── go.sum
│   └── Dockerfile
│
├── service-b/                      ← Service Rekam Medis
│   ├── cmd/main.go
│   ├── internal/
│   │   ├── db/postgres.go          ← Koneksi db_rekam_medis
│   │   ├── grpc/
│   │   │   ├── server.go           ← gRPC server: CheckPatientRecord
│   │   │   └── codec.go            ← JSON codec workaround untuk .pb.go manual
│   │   ├── handler/record.go       ← GET /api/records, GET /api/records/:nik
│   │   ├── mq/consumer.go          ← Consume event, buat draft rekam medis
│   │   └── proto/                  ← Generated stubs dari medical_record.proto
│   ├── go.mod
│   ├── go.sum
│   └── Dockerfile
│
├── frontend/                       ← UI React
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   │       ├── PatientForm.jsx     ← Form pendaftaran pasien
│   │       └── PatientList.jsx     ← Tabel daftar pasien
│   ├── package.json
│   ├── package-lock.json
│   └── Dockerfile
│
├── docker-compose.yml              ← Orkestrasi 5 container
├── init-db.sql                     ← Inisialisasi db_pendaftaran + db_rekam_medis
│
├── MediSync-Diagram.drawio         ← Diagram arsitektur (berwarna)
├── MediSync-Diagram-BW.drawio      ← Diagram arsitektur (hitam-putih, untuk laporan)
├── LAPORAN_MEDISYNC.md             ← Laporan lengkap dalam Markdown
├── LAPORAN_MEDISYNC.docx           ← Laporan dalam format Word
├── MediSync-Presentasi-NEW.pptx    ← Slide presentasi 12 halaman
│
├── generate_docs.py                ← Script generator laporan+PPT (bukti AI usage)
├── PROMPT_VIBECODE_IMPLEMENTASI.md ← Prompt AI untuk implementasi (bukti AI usage)
└── PROMPT_VIBECODE_LAPORAN_WORD.md ← Prompt AI untuk laporan (bukti AI usage)
```

---

## Cara Menjalankan (dengan Makefile)

```bash
make run       # build dan jalankan semua service
make down      # hentikan semua container
make reset     # reset data + jalankan ulang
make logs      # lihat log semua service
make proto     # regenerate .pb.go dari proto/medical_record.proto
make help      # lihat semua perintah
```

## Cara Menjalankan (tanpa Make)

### Prasyarat

- Docker Desktop terinstall dan berjalan
- Port berikut tidak dipakai: `3000`, `4001`, `4002`, `50052`, `5432`, `5672`, `15672`

### Jalankan

```bash
# Clone repository
git clone <repo-url>
cd MediSync

# Build dan jalankan semua service
docker compose up --build

# Atau jalankan di background
docker compose up --build -d
```

Tunggu hingga log menampilkan:
```
[Service-A][DB] Tabel patients siap.
[Service-B][DB] Tabel medical_records siap.
[Service-B][MQ] Consumer aktif. Mendengarkan queue 'patient.queue'...
[Service-B][gRPC] gRPC server berjalan di port 50052
```

### Akses

| Layanan | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Service A Health | http://localhost:4001/health |
| Service B Health | http://localhost:4002/health |
| RabbitMQ UI | http://localhost:15672 (guest / guest) |

### Reset Data

```bash
docker compose down -v   # hapus semua container + volume
docker compose up --build
```

---

## API Reference

### Service A — Pendaftaran (:4001)

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `POST` | `/api/patients` | Daftarkan pasien baru |
| `GET` | `/api/patients` | Ambil semua data pasien |
| `GET` | `/health` | Health check |

**Contoh request pendaftaran:**
```bash
curl -X POST http://localhost:4001/api/patients \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Budi Santoso",
    "nik": "3201234567890001",
    "tanggal_lahir": "1990-05-15",
    "no_telepon": "08123456789"
  }'
```

### Service B — Rekam Medis (:4002)

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `GET` | `/api/records` | Ambil semua rekam medis |
| `GET` | `/api/records/:nik` | Ambil rekam medis by NIK |
| `GET` | `/health` | Health check |

---

## Alur Data End-to-End

```
1. User isi form pasien di Frontend (React)
        ↓ HTTP POST /api/patients
2. Service A validasi input
        ↓ gRPC CheckPatientRecord(nik) — SYNCHRONOUS — Service A menunggu
3. Service B query db_rekam_medis → return has_record true/false
        ↓ Jika sudah ada: HTTP 409 Conflict (tolak)
        ↓ Jika belum ada:
4. Service A INSERT ke db_pendaftaran
        ↓ gRPC berhasil → simpan lokal selesai
5. Service A publish event "patient.registered" ke RabbitMQ — ASYNCHRONOUS
        ↓ Service A langsung return HTTP 201 ke Frontend (tidak menunggu B)
6. Service B consume event dari queue "patient.queue"
        ↓ INSERT draft rekam medis ke db_rekam_medis
7. Draft rekam medis tersedia di GET /api/records/:nik
```

---

## Pemenuhan Requirement Tugas

| Requirement | Status | Bukti |
|-------------|--------|-------|
| Frontend input data pasien | ✅ PASS | `frontend/src/components/PatientForm.jsx` |
| Service A + database sendiri | ✅ PASS | `service-a/internal/db/postgres.go` → `db_pendaftaran` |
| Service B + database sendiri | ✅ PASS | `service-b/internal/db/postgres.go` → `db_rekam_medis` |
| gRPC Synchronous | ✅ PASS | `service-a/internal/grpc/client.go` + `service-b/internal/grpc/server.go` |
| RabbitMQ Asynchronous | ✅ PASS | `service-a/internal/mq/producer.go` + `service-b/internal/mq/consumer.go` |
| Database Isolation | ✅ PASS | Zero cross-DB query di seluruh codebase |
| Contract-First (.proto) | ✅ PASS | `proto/medical_record.proto` sebagai single source of truth |
| Bisa dijalankan lokal | ✅ PASS | `docker compose up --build` |

---

## Catatan Teknis

### Contract-First & Regenerasi Proto

Kontrak gRPC didefinisikan di `proto/medical_record.proto` sebagai **single source of truth**.
File stub `.pb.go` yang ada di `service-a/internal/proto/` dan `service-b/internal/proto/` ditulis secara manual untuk keperluan tugas ini.

Untuk regenerasi menggunakan `protoc` (cara yang benar di proyek nyata):
```bash
# Install protoc tools dulu:
# https://grpc.io/docs/languages/go/quickstart/

make proto
# atau manual:
protoc \
  --go_out=service-a/internal/proto --go_opt=paths=source_relative \
  --go-grpc_out=service-a/internal/proto --go-grpc_opt=paths=source_relative \
  --proto_path=proto proto/medical_record.proto
```

### Kenapa ada `codec.go` di `internal/grpc/`?

File `.pb.go` manual tidak mengimplementasikan protobuf binary descriptor secara lengkap (`ProtoReflect()` tidak menghasilkan descriptor bytes). Tanpa descriptor, gRPC tidak bisa melakukan serialisasi biner dan akan crash dengan error `nil message`.

`codec.go` menyelesaikan ini dengan mendaftarkan **JSON codec** sebagai pengganti codec `"proto"` default gRPC:

```
Tanpa codec.go:  gRPC → proto.Marshal(msg) → ProtoReflect() → nil → CRASH
Dengan codec.go: gRPC → json.Marshal(msg)  → {"nik":"..."} → OK ✓
```

Kontrak tetap didefinisikan di `proto/medical_record.proto`. Service name, method name, dan field names tetap persis sama — hanya format wire yang berubah dari biner ke JSON. Ini **tidak mengubah semantik gRPC**, hanya mengubah transport encoding.

### Ketahanan MQ (Reconnect Otomatis)

- **Service B consumer** (`service-b/internal/mq/consumer.go`): menggunakan outer reconnect loop. Jika RabbitMQ restart saat runtime, consumer mendeteksi koneksi putus via `NotifyClose` dan reconnect otomatis setiap 5 detik.
- **Service A producer** (`service-a/internal/mq/producer.go`): jika publish gagal karena channel putus, mencoba reconnect sekali sebelum return error.

---

## Troubleshooting

| Masalah | Solusi |
|---------|--------|
| Container gagal start | Pastikan Docker Desktop running, cek port tidak bentrok |
| Service A return 503 | Pastikan service-b dan RabbitMQ sudah fully ready (tunggu ~30 detik) |
| Data tidak muncul di Service B | Tunggu consumer MQ memproses (~2-3 detik setelah pendaftaran) |
| Reset data | `docker compose down -v && docker compose up --build` |

---

*MediSync — Tugas Jaringan Komputer Terapan 2025/2026*
