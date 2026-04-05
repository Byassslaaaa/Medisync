# MediSync — Makefile
# Jalankan perintah di bawah dari root project (folder MediSync/)

.PHONY: proto run run-bg down reset logs logs-a logs-b logs-db-a logs-db-b verify-isolation help

# ─── gRPC: Regenerate file .pb.go dari proto/medical_record.proto ─────────────
# Prasyarat: protoc + plugin protoc-gen-go + protoc-gen-go-grpc terinstall
# Install: https://grpc.io/docs/languages/go/quickstart/
proto:
	@echo "[proto] Generating Go stubs dari proto/medical_record.proto ..."
	protoc \
		--go_out=service-a/internal/proto \
		--go_opt=paths=source_relative \
		--go-grpc_out=service-a/internal/proto \
		--go-grpc_opt=paths=source_relative \
		--proto_path=proto \
		proto/medical_record.proto
	cp service-a/internal/proto/medical_record.pb.go     service-b/internal/proto/medical_record.pb.go
	cp service-a/internal/proto/medical_record_grpc.pb.go service-b/internal/proto/medical_record_grpc.pb.go
	@echo "[proto] Done. Stubs tersedia di service-a/internal/proto/ dan service-b/internal/proto/"

# ─── Docker Compose ────────────────────────────────────────────────────────────
run:
	docker compose up --build

run-bg:
	docker compose up --build -d

down:
	docker compose down

reset:
	docker compose down -v
	docker compose up --build

logs:
	docker compose logs -f

logs-a:
	docker compose logs -f service-a

logs-b:
	docker compose logs -f service-b

logs-db-a:
	docker compose logs -f postgres-a

logs-db-b:
	docker compose logs -f postgres-b

# ─── Verifikasi isolasi database (jalankan setelah 'make run-bg') ──────────────
# Membuktikan bahwa Service A dan B benar-benar menggunakan instance PostgreSQL berbeda.
verify-isolation:
	@echo ""
	@echo "=== Verifikasi Isolasi Database Fisik ==="
	@echo ""
	@echo "[1] Tabel di postgres-a (db_pendaftaran):"
	docker exec medisync-postgres-a psql -U admin -d db_pendaftaran -c "\dt"
	@echo ""
	@echo "[2] Tabel di postgres-b (db_rekam_medis):"
	docker exec medisync-postgres-b psql -U admin -d db_rekam_medis -c "\dt"
	@echo ""
	@echo "[3] Data patients di postgres-a:"
	docker exec medisync-postgres-a psql -U admin -d db_pendaftaran -c "SELECT id, name, nik, created_at FROM patients ORDER BY created_at DESC LIMIT 5;"
	@echo ""
	@echo "[4] Data medical_records di postgres-b:"
	docker exec medisync-postgres-b psql -U admin -d db_rekam_medis -c "SELECT id, name, nik, diagnosis, created_at FROM medical_records ORDER BY created_at DESC LIMIT 5;"
	@echo ""
	@echo "=== Selesai. Dua database fisik terkonfirmasi terpisah. ==="

# ─── Help ──────────────────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "MediSync — Perintah yang tersedia:"
	@echo ""
	@echo "  make proto             Regenerate .pb.go dari proto/medical_record.proto"
	@echo "  make run               Build dan jalankan semua service (foreground)"
	@echo "  make run-bg            Build dan jalankan semua service (background)"
	@echo "  make down              Hentikan semua container"
	@echo "  make reset             Hentikan + hapus volume + jalankan ulang (reset data)"
	@echo "  make logs              Lihat log semua service"
	@echo "  make logs-a            Lihat log Service A saja"
	@echo "  make logs-b            Lihat log Service B saja"
	@echo "  make logs-db-a         Lihat log postgres-a (db_pendaftaran)"
	@echo "  make logs-db-b         Lihat log postgres-b (db_rekam_medis)"
	@echo "  make verify-isolation  Verifikasi isolasi fisik kedua database"
	@echo ""
