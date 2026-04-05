package main

import (
	"log"
	"os"

	"hospital/service-b/internal/db"
	grpcserver "hospital/service-b/internal/grpc"
	"hospital/service-b/internal/handler"
	"hospital/service-b/internal/mq"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func main() {
	log.Println("========================================")
	log.Println("  MediSync — Service B (Rekam Medis)  ")
	log.Println("========================================")

	// 1. Inisialisasi koneksi database
	db.Connect()

	// 2. Jalankan gRPC server di goroutine terpisah
	// Goroutine memungkinkan gRPC server dan HTTP server berjalan bersamaan
	go grpcserver.Start()

	// 3. Jalankan RabbitMQ consumer di goroutine terpisah
	// Consumer mendengarkan event secara terus-menerus tanpa memblok server
	go mq.Start()

	// 4. Setup HTTP server
	r := gin.Default()

	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:3000", "http://localhost"},
		AllowMethods:     []string{"GET", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type"},
		AllowCredentials: true,
	}))

	r.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{"status": "ok", "service": "service-b"})
	})

	api := r.Group("/api")
	{
		api.GET("/records", handler.GetAllRecords)
		api.GET("/records/:nik", handler.GetRecordByNIK)
	}

	port := os.Getenv("PORT")
	if port == "" {
		port = "4002"
	}

	log.Printf("[Service-B] HTTP server berjalan di port %s", port)
	if err := r.Run(":" + port); err != nil {
		log.Fatalf("[Service-B] Server error: %v", err)
	}
}
