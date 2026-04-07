package grpcclient

import (
	"context"
	"fmt"
	"log"
	"os"
	"sync"
	"time"

	pb "hospital/service-a/internal/proto"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

var (
	client     pb.MedicalRecordServiceClient
	grpcConn   *grpc.ClientConn
	grpcTarget string
	mu         sync.Mutex
)

// Connect membuka koneksi gRPC ke Service B dengan retry logic.
func Connect() {
	grpcTarget = os.Getenv("GRPC_SERVICE_B")
	if grpcTarget == "" {
		grpcTarget = "localhost:50052"
	}

	if err := connectWithRetry(3, 2*time.Second); err != nil {
		// Jangan hentikan service-a jika service-b belum tersedia.
		log.Printf("[Service-A][gRPC] Service B belum tersedia saat startup: %v", err)
		log.Printf("[Service-A][gRPC] Service A tetap berjalan. Koneksi gRPC akan dicoba ulang saat ada request.")
		return
	}

	log.Printf("[Service-A][gRPC] Koneksi ke Service B (%s) berhasil.", grpcTarget)
}

func connectWithRetry(maxRetry int, delay time.Duration) error {
	mu.Lock()
	defer mu.Unlock()

	if client != nil {
		return nil
	}

	var lastErr error
	for i := 0; i < maxRetry; i++ {
		ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
		conn, err := grpc.DialContext(
			ctx,
			grpcTarget,
			grpc.WithTransportCredentials(insecure.NewCredentials()),
			grpc.WithBlock(),
		)
		cancel()

		if err == nil {
			grpcConn = conn
			client = pb.NewMedicalRecordServiceClient(conn)
			return nil
		}

		lastErr = err
		log.Printf("[Service-A][gRPC] Gagal connect ke Service B, retry ke-%d: %v", i+1, err)
		time.Sleep(delay)
	}

	return fmt.Errorf("tidak bisa connect ke Service B setelah %d retry: %w", maxRetry, lastErr)
}

func ensureClient() error {
	if client != nil {
		return nil
	}
	return connectWithRetry(2, 1*time.Second)
}

func markClientUnavailable() {
	mu.Lock()
	defer mu.Unlock()
	client = nil
	if grpcConn != nil {
		_ = grpcConn.Close()
		grpcConn = nil
	}
}

// GetAllRecords memanggil Service B via gRPC untuk mengambil semua rekam medis.
// Ini adalah komunikasi SYNCHRONOUS — digunakan saat frontend request daftar rekam medis.
func GetAllRecords() ([]*pb.MedicalRecordItem, error) {
	if err := ensureClient(); err != nil {
		return nil, err
	}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	log.Println("[Service-A][gRPC] → Memanggil GetAllRecords ke Service B")

	resp, err := client.GetAllRecords(ctx, &pb.GetRecordsRequest{})
	if err != nil {
		markClientUnavailable()
		log.Printf("[Service-A][gRPC] ✗ Error GetAllRecords dari Service B: %v", err)
		return nil, err
	}

	log.Printf("[Service-A][gRPC] ← Menerima %d rekam medis dari Service B", len(resp.GetRecords()))
	return resp.GetRecords(), nil
}

// CheckPatientRecord memanggil Service B via gRPC untuk cek apakah pasien sudah punya rekam medis.
// Ini adalah komunikasi SYNCHRONOUS — Service A menunggu respons sebelum lanjut.
func CheckPatientRecord(nik string) (bool, string, error) {
	if err := ensureClient(); err != nil {
		return false, "", err
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	log.Printf("[Service-A][gRPC] → Memanggil CheckPatientRecord untuk NIK: %s", nik)

	resp, err := client.CheckPatientRecord(ctx, &pb.PatientRequest{Nik: nik})
	if err != nil {
		markClientUnavailable()
		log.Printf("[Service-A][gRPC] ✗ Error dari Service B: %v", err)
		return false, "", err
	}

	log.Printf("[Service-A][gRPC] ← Response dari Service B: has_record=%v, message=%s", resp.HasRecord, resp.Message)
	return resp.HasRecord, resp.RecordId, nil
}
