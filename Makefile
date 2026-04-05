# MediSync — Makefile
# Jalankan perintah di bawah dari root project (folder MediSync/)

.PHONY: proto run down reset logs help

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

# ─── Help ──────────────────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "MediSync — Perintah yang tersedia:"
	@echo ""
	@echo "  make proto     Regenerate .pb.go dari proto/medical_record.proto"
	@echo "  make run       Build dan jalankan semua service (foreground)"
	@echo "  make run-bg    Build dan jalankan semua service (background)"
	@echo "  make down      Hentikan semua container"
	@echo "  make reset     Hentikan + hapus volume + jalankan ulang (reset data)"
	@echo "  make logs      Lihat log semua service"
	@echo "  make logs-a    Lihat log Service A saja"
	@echo "  make logs-b    Lihat log Service B saja"
	@echo ""
