package main

import (
	"log"
	"os"

	"hospital/service-a/internal/db"
	grpcclient "hospital/service-a/internal/grpc"
	"hospital/service-a/internal/handler"
	"hospital/service-a/internal/mq"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func main() {
	log.Println("========================================")
	log.Println("  MediSync — Service A (Pendaftaran)   ")
	log.Println("========================================")

	// 1. Inisialisasi koneksi database
	db.Connect()

	// 2. Inisialisasi koneksi gRPC ke Service B
	grpcclient.Connect()

	// 3. Inisialisasi koneksi RabbitMQ
	mq.Connect()

	// 4. Setup HTTP server dengan Gin
	r := gin.Default()

	// CORS middleware — izinkan request dari Frontend (localhost:3000)
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:3000", "http://localhost"},
		AllowMethods:     []string{"GET", "POST", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Accept"},
		AllowCredentials: true,
	}))

	// Health check
	r.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{"status": "ok", "service": "service-a"})
	})

	// API routes
	api := r.Group("/api")
	{
		api.POST("/patients", handler.RegisterPatient)
		api.GET("/patients", handler.GetAllPatients)
	}

	port := os.Getenv("PORT")
	if port == "" {
		port = "4001"
	}

	log.Printf("[Service-A] Server berjalan di port %s", port)
	if err := r.Run(":" + port); err != nil {
		log.Fatalf("[Service-A] Server error: %v", err)
	}
}
