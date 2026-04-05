# MediSync — Implementasi Komunikasi Microservices

> **Tugas Jaringan Komputer Terapan | Semester Genap 2025/2026**
>
> Studi kasus: Sistem Informasi Rumah Sakit berbasis arsitektur **Microservices**
> dengan komunikasi **gRPC (sinkron)** dan **RabbitMQ (asinkron)**.
> Database dipisah **secara fisik** — dua instance PostgreSQL berbeda.

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
┌──────────────────────────────────────────────────────────────────────┐
│                     Docker Network: medisync-net                     │
│                                                                      │
│  ┌──────────────┐  HTTP/REST  ┌──────────────────────────────────┐  │
│  │   Frontend   │────────────►│           Service A              │  │
│  │ React + Vite │  POST /api  │  Pendaftaran | Port 4001         │  │
│  │  Port: 3000  │             └──────────┬───────────────────────┘  │
│  └──────────────┘                        │                           │
│                              ┌───────────┤                           │
│                         gRPC │     MQ    │                           │
│                        (sync)│  (async)  │                           │
│                              ▼           ▼                           │
│                   ┌──────────────────┐  ┌──────────┐                │
│                   │    Service B     │◄─┤ RabbitMQ │                │
│                   │  Rekam Medis     │  │  :5672   │                │
│                   │  :4002 / :50052  │  │ UI:15672 │                │
│                   └──────────────────┘  └──────────┘                │
│                          │                                           │
│          ┌───────────────┴──────────────────────────┐               │
│          │                                          │               │
│   ┌──────▼──────────────────┐  ┌───────────────────▼─────────┐     │
│   │      postgres-a         │  │         postgres-b           │     │
│   │  db_pendaftaran         │  │     db_rekam_medis           │     │
│   │  host port: 5433        │  │     host port: 5434          │     │
│   │  ← Service A ONLY →     │  │     ← Service B ONLY →      │     │
│   └─────────────────────────┘  └─────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Komponen | Teknologi | Port (Host) | Port (Container) |
|----------|-----------|-------------|-----------------|
| Frontend | React 18 + Vite + Axios | 3000 | 80 |
| Service A | Go 1.21 + Gin + gRPC Client | 4001 | 4001 |
| Service B | Go 1.21 + Gin + gRPC Server | 4002 / 50052 | 4002 / 50052 |
| **postgres-a** | **PostgreSQL 15 — `db_pendaftaran`** | **5433** | **5432** |
| **postgres-b** | **PostgreSQL 15 — `db_rekam_medis`** | **5434** | **5432** |
| Message Broker | RabbitMQ 3.12 | 5672 / 15672 | 5672 / 15672 |
| Deployment | Docker Compose | — | — |

---

## Database Isolation (Physical Separation)

MediSync menggunakan **dua instance PostgreSQL terpisah** — bukan satu server dengan dua database.

| | postgres-a | postgres-b |
|---|---|---|
| **Container** | `medisync-postgres-a` | `medisync-postgres-b` |
| **Database** | `db_pendaftaran` | `db_rekam_medis` |
| **Volume** | `pgdata-a` | `pgdata-b` |
| **Init script** | `init-db-a.sql` | `init-db-b.sql` |
| **Host port** | `5433` | `5434` |
| **Dapat diakses oleh** | Service A **saja** | Service B **saja** |

### Checklist Verifikasi Isolasi

- [ ] `service-a` hanya punya env `DB_URL` yang mengarah ke `postgres-a:5432`
- [ ] `service-b` hanya punya env `DB_URL` yang mengarah ke `postgres-b:5432`
- [ ] Tidak ada query cross-DB di seluruh codebase
- [ ] `depends_on` service-a hanya menyebut `postgres-a`, service-b hanya menyebut `postgres-b`
- [ ] Volume `pgdata-a` dan `pgdata-b` berdiri sendiri — satu volume tidak bisa dibaca instance lain

Jalankan `make verify-isolation` setelah sistem up untuk membuktikan pemisahan fisik.

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
│   │   ├── db/postgres.go          ← Koneksi ke postgres-a / db_pendaftaran
│   │   ├── grpc/
│   │   │   ├── client.go           ← gRPC client ke Service B
│   │   │   └── codec.go            ← JSON codec workaround untuk .pb.go manual
│   │   ├── handler/patient.go      ← POST /api/patients, GET /api/patients
│   │   ├── mq/producer.go          ← Publish event patient.registered
│   │   └── proto/                  ← Generated stubs dari medical_record.proto
│   ├── go.mod / go.sum
│   └── Dockerfile
│
├── service-b/                      ← Service Rekam Medis
│   ├── cmd/main.go
│   ├── internal/
│   │   ├── db/postgres.go          ← Koneksi ke postgres-b / db_rekam_medis
│   │   ├── grpc/
│   │   │   ├── server.go           ← gRPC server: CheckPatientRecord
│   │   │   └── codec.go            ← JSON codec workaround untuk .pb.go manual
│   │   ├── handler/record.go       ← GET /api/records, GET /api/records/:nik
│   │   ├── mq/consumer.go          ← Consume event, buat draft rekam medis
│   │   └── proto/                  ← Generated stubs dari medical_record.proto
│   ├── go.mod / go.sum
│   └── Dockerfile
│
├── frontend/                       ← UI React
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   │       ├── PatientForm.jsx     ← Form pendaftaran pasien
│   │       └── PatientList.jsx     ← Tabel daftar pasien
│   ├── package.json / package-lock.json
│   └── Dockerfile
│
├── docker-compose.yml              ← Orkestrasi 6 container (termasuk 2 postgres)
├── init-db-a.sql                   ← Init pgcrypto untuk postgres-a
├── init-db-b.sql                   ← Init pgcrypto untuk postgres-b
├── Makefile                        ← Shortcut perintah + verify-isolation
└── README.md
```

---

## Cara Menjalankan (dengan Makefile)

```bash
make run              # build dan jalankan semua service (foreground)
make run-bg           # build dan jalankan semua service (background)
make down             # hentikan semua container
make reset            # reset data + jalankan ulang
make logs             # lihat log semua service
make logs-a           # log Service A
make logs-b           # log Service B
make logs-db-a        # log postgres-a
make logs-db-b        # log postgres-b
make verify-isolation # verifikasi pemisahan fisik database
make proto            # regenerate .pb.go dari proto/medical_record.proto
make help             # lihat semua perintah
```

## Cara Menjalankan (tanpa Make)

### Prasyarat

- Docker Desktop terinstall dan berjalan
- Port berikut tidak dipakai: `3000`, `4001`, `4002`, `50052`, `5433`, `5434`, `5672`, `15672`

> **Catatan Port Database**: postgres-a di-expose ke host port `5433`, postgres-b ke port `5434`.
> Ini untuk menghindari konflik dengan instalasi PostgreSQL lokal yang biasanya ada di port `5432`.

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
docker compose down -v   # hapus semua container + kedua volume
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
3. Service B query db_rekam_medis di postgres-b → return has_record true/false
        ↓ Jika sudah ada: HTTP 409 Conflict (tolak)
        ↓ Jika belum ada:
4. Service A INSERT ke db_pendaftaran di postgres-a
        ↓ simpan lokal selesai
5. Service A publish event "patient.registered" ke RabbitMQ — ASYNCHRONOUS
        ↓ Service A langsung return HTTP 201 ke Frontend (tidak menunggu B)
6. Service B consume event dari queue "patient.queue"
        ↓ INSERT draft rekam medis ke db_rekam_medis di postgres-b
7. Draft rekam medis tersedia di GET /api/records/:nik
```

---

## Pemenuhan Requirement Tugas

| Requirement | Status | Bukti |
|-------------|--------|-------|
| Frontend input data pasien | ✅ PASS | `frontend/src/components/PatientForm.jsx` |
| Service A + database sendiri | ✅ PASS | `service-a` → `postgres-a` / `db_pendaftaran` |
| Service B + database sendiri | ✅ PASS | `service-b` → `postgres-b` / `db_rekam_medis` |
| gRPC Synchronous | ✅ PASS | `service-a/internal/grpc/client.go` + `service-b/internal/grpc/server.go` |
| RabbitMQ Asynchronous | ✅ PASS | `service-a/internal/mq/producer.go` + `service-b/internal/mq/consumer.go` |
| **Database Isolation Fisik** | ✅ **PASS** | **Dua container PostgreSQL terpisah: `postgres-a` & `postgres-b`** |
| Contract-First (.proto) | ✅ PASS | `proto/medical_record.proto` sebagai single source of truth |
| Bisa dijalankan lokal | ✅ PASS | `docker compose up --build` |

---

## Catatan Teknis

### Pemisahan Database Fisik

Arsitektur lama menggunakan **satu instance PostgreSQL** dengan dua database (`db_pendaftaran` dan `db_rekam_medis`) di dalamnya. Secara logis terpisah, tetapi secara fisik masih satu server.

Arsitektur baru menggunakan **dua container PostgreSQL terpisah**:
- `postgres-a` hanya berisi `db_pendaftaran` — dikontrol eksklusif oleh Service A
- `postgres-b` hanya berisi `db_rekam_medis` — dikontrol eksklusif oleh Service B

Implikasi nyata:
- Dua proses `postgres` berjalan secara independen di container berbeda
- Dua volume Docker berbeda (`pgdata-a`, `pgdata-b`) — tidak ada shared storage
- Jika salah satu postgres container down, service pasangannya down, service lain tetap jalan
- Credential, konfigurasi, dan lifecycle masing-masing DB bisa dikelola secara independen

### Contract-First & Regenerasi Proto

Kontrak gRPC didefinisikan di `proto/medical_record.proto` sebagai **single source of truth**.

Untuk regenerasi menggunakan `protoc`:
```bash
make proto
```

### Kenapa ada `codec.go` di `internal/grpc/`?

File `.pb.go` manual tidak mengimplementasikan protobuf binary descriptor secara lengkap (`ProtoReflect()` tidak menghasilkan descriptor bytes). `codec.go` menyelesaikan ini dengan mendaftarkan **JSON codec** sebagai pengganti codec `"proto"` default gRPC:

```
Tanpa codec.go:  gRPC → proto.Marshal(msg) → ProtoReflect() → nil → CRASH
Dengan codec.go: gRPC → json.Marshal(msg)  → {"nik":"..."} → OK ✓
```

### Ketahanan MQ (Reconnect Otomatis)

- **Service B consumer** (`service-b/internal/mq/consumer.go`): menggunakan outer reconnect loop. Jika RabbitMQ restart saat runtime, consumer mendeteksi koneksi putus via `NotifyClose` dan reconnect otomatis setiap 5 detik.
- **Service A producer** (`service-a/internal/mq/producer.go`): jika publish gagal karena channel putus, mencoba reconnect sekali sebelum return error.

---

## Troubleshooting

| Masalah | Solusi |
|---------|--------|
| Container gagal start | Pastikan Docker Desktop running, cek port 5433/5434/5672 tidak bentrok |
| Service A return 503 | Pastikan service-b, postgres-a, dan RabbitMQ sudah fully ready (tunggu ~30 detik) |
| Data tidak muncul di Service B | Tunggu consumer MQ memproses (~2-3 detik setelah pendaftaran) |
| Reset data | `docker compose down -v && docker compose up --build` |
| Verifikasi isolasi DB | `make verify-isolation` |

---

*MediSync — Tugas Jaringan Komputer Terapan 2025/2026*
