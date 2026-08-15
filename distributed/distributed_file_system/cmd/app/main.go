package main

import (
	"context"
	"fmt"
	"io/ioutil"
	"log"
	"os"

	"github.com/minio/minio-go/v7"
	"github.com/minio/minio-go/v7/pkg/credentials"
)

func main() {
	endpoint := "localhost:9000"
	accessKeyID := "admin"
	secretAccessKey := "password"
	useSSL := false

	// Inisialisasi MinIO Client
	minioClient, err := minio.New(endpoint, &minio.Options{
		Creds:  credentials.NewStaticV4(accessKeyID, secretAccessKey, ""),
		Secure: useSSL,
	})
	if err != nil {
		log.Fatalln(err)
	}
	log.Println("✅ Berhasil terhubung ke MinIO Object Storage")

	ctx := context.Background()
	bucketName := "storage-terdistribusi"
	location := "us-east-1"

	// 1. Buat Bucket (jika belum ada)
	err = minioClient.MakeBucket(ctx, bucketName, minio.MakeBucketOptions{Region: location})
	if err != nil {
		// Cek apakah bucket sudah ada
		exists, errBucketExists := minioClient.BucketExists(ctx, bucketName)
		if errBucketExists == nil && exists {
			log.Printf("📦 Bucket '%s' sudah ada.\n", bucketName)
		} else {
			log.Fatalln(err)
		}
	} else {
		log.Printf("🎉 Berhasil membuat bucket baru: '%s'\n", bucketName)
	}

	// Buat file dummy lokal untuk diupload
	localFilePath := "/tmp/file-super-besar.txt"
	fileContent := []byte("Ini adalah simulasi file video raksasa berukuran 10GB yang akan di-chunk dan di-upload ke MinIO oleh aplikasi.")
	err = ioutil.WriteFile(localFilePath, fileContent, 0644)
	if err != nil {
		log.Fatalf("Gagal membuat file dummy: %v", err)
	}
	defer os.Remove(localFilePath)

	// 2. Upload file (PutObject)
	objectName := "video/tutorial-golang.txt"
	contentType := "text/plain"

	log.Printf("📤 Sedang meng-upload '%s' ke bucket '%s'...", objectName, bucketName)
	
	// FPutObject secara otomatis melakukan "Chunking" (Multipart Upload) jika file sangat besar
	info, err := minioClient.FPutObject(ctx, bucketName, objectName, localFilePath, minio.PutObjectOptions{ContentType: contentType})
	if err != nil {
		log.Fatalln(err)
	}
	log.Printf("✅ Upload selesai! Ukuran: %d bytes\n", info.Size)

	// 3. Baca File dari Storage (GetObject)
	log.Printf("📥 Mencoba men-download kembali file '%s'...", objectName)
	obj, err := minioClient.GetObject(ctx, bucketName, objectName, minio.GetObjectOptions{})
	if err != nil {
		log.Fatalln(err)
	}
	defer obj.Close()
	
	downloadedContent, err := ioutil.ReadAll(obj)
	if err != nil {
		log.Fatalln(err)
	}
	fmt.Printf("\n--- ISI FILE YANG DIDOWNLOAD ---\n%s\n--------------------------------\n", string(downloadedContent))
}
