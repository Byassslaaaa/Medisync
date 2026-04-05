package grpcclient

import (
	"context"
	"log"
	"os"
	"time"

	pb "hospital/service-a/internal/proto"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

var client pb.MedicalRecordServiceClient

// Connect membuka koneksi gRPC ke Service B dengan retry logic.
func Connect() {
	target := os.Getenv("GRPC_SERVICE_B")
	if target == "" {
		target = "localhost:50052"
	}

	var conn *grpc.ClientConn
	var err error

	for i := 0; i < 10; i++ {
		conn, err = grpc.Dial(target, grpc.WithTransportCredentials(insecure.NewCredentials()))
		if err == nil {
			break
		}
		log.Printf("[Service-A][gRPC] Gagal connect ke Service B, retry ke-%d...", i+1)
		time.Sleep(3 * time.Second)
	}

	if err != nil {
		log.Fatalf("[Service-A][gRPC] Tidak bisa connect ke Service B: %v", err)
	}

	client = pb.NewMedicalRecordServiceClient(conn)
	log.Printf("[Service-A][gRPC] Koneksi ke Service B (%s) berhasil.", target)
}

// CheckPatientRecord memanggil Service B via gRPC untuk cek apakah pasien sudah punya rekam medis.
// Ini adalah komunikasi SYNCHRONOUS — Service A menunggu respons sebelum lanjut.
func CheckPatientRecord(nik string) (bool, string, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	log.Printf("[Service-A][gRPC] → Memanggil CheckPatientRecord untuk NIK: %s", nik)

	resp, err := client.CheckPatientRecord(ctx, &pb.PatientRequest{Nik: nik})
	if err != nil {
		log.Printf("[Service-A][gRPC] ✗ Error dari Service B: %v", err)
		return false, "", err
	}

	log.Printf("[Service-A][gRPC] ← Response dari Service B: has_record=%v, message=%s", resp.HasRecord, resp.Message)
	return resp.HasRecord, resp.RecordId, nil
}
