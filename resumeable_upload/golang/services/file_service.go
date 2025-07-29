package services

import (
	"context"
	"fmt"
	"io"
	"mime"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

type FileService interface {
	Upload(ctx context.Context, fileId string, chunkIndex string, body io.ReadCloser) string
	Merge(ctx context.Context, fileId string, totalChunks int) string
	CheckFile(ctx context.Context, fileId string) ([]int, error)
	UploadAndMerge(ctx context.Context, fileId string, chunkIndex string, lastChunkIndex string, body io.ReadCloser) (response map[string]interface{})
}

type fileService struct {
}

func NewFileService() FileService {
	return &fileService{}
}

func (service *fileService) Upload(ctx context.Context, fileId string, chunkIndex string, body io.ReadCloser) string {
	temporaryPath := fmt.Sprintf("uploads/%s.part%s", fileId, chunkIndex)
	file, err := os.Create(temporaryPath)
	if err != nil {
		return err.Error()
	}
	defer file.Close()

	_, err = io.Copy(file, body)
	if err != nil {
		return err.Error()
	}

	return "success upload"
}

func (service *fileService) Merge(ctx context.Context, fileId string, totalChunks int) string {
	outputFilePatch := fmt.Sprintf("uploads/" + fileId + ".merged")
	outputFile, err := os.Create(outputFilePatch)
	if err != nil {
		return err.Error()
	}
	defer outputFile.Close()

	for i := 0; i < totalChunks; i++ {
		chunkPath := fmt.Sprintf("uploads/%s.part%d", fileId, i)
		chunkFile, err := os.Open(chunkPath)
		if err != nil {
			return err.Error()
		}
		io.Copy(outputFile, chunkFile)
		chunkFile.Close()
		os.Remove(chunkPath)
	}

	buffer := make([]byte, 512)
	outputFile.Seek(0, io.SeekStart)
	_, err = outputFile.Read(buffer)
	if err != nil {
		return err.Error()
	}
	mimeType := http.DetectContentType(buffer)
	extention := ".bin"
	extentions, err := mime.ExtensionsByType(mimeType)
	fmt.Println("extentions:", extentions)
	if err != nil {
		return err.Error()
	}
	if len(extentions) > 0 {
		extention = extentions[0]
	}
	// you can check the extention file here

	finalPath := fmt.Sprintf("uploads/%s%s", fileId, extention)
	err = os.Rename(outputFilePatch, finalPath)
	if err != nil {
		return err.Error()
	}
	return "success merge"
}

func (service *fileService) CheckFile(ctx context.Context, fileId string) ([]int, error) {
	pattern := fmt.Sprintf("uploads/%s.part*", fileId)
	matches, err := filepath.Glob(pattern)
	if err != nil {
		return []int{}, err
	}
	var indices []int
	for _, path := range matches {
		base := filepath.Base(path)
		parts := strings.Split(base, ".part")
		if len(parts) == 2 {
			index, err := strconv.Atoi(parts[1])
			if err != nil {
				return []int{}, err
			}
			indices = append(indices, index)
		}
	}
	return indices, nil
}

func (service *fileService) UploadAndMerge(ctx context.Context, fileId string, chunkIndex string, lastChunkIndex string, body io.ReadCloser) (response map[string]interface{}) {
	var err error

	// from file header multipart file header (upload by user through http) you cannot directly merge it into file, you have to save it to disk, open it and then merge it
	temporaryPath := fmt.Sprintf("uploads/%s.temp%s", fileId, chunkIndex)
	file, err := os.Create(temporaryPath)
	if err != nil {
		return map[string]interface{}{
			"response": err.Error(),
		}
	}
	defer file.Close()
	_, err = io.Copy(file, body)
	if err != nil {
		return map[string]interface{}{
			"response": err.Error(),
		}
	}

	tempFile, err := os.Open(temporaryPath)
	if err != nil {
		return map[string]interface{}{
			"response": err.Error(),
		}
	}
	defer tempFile.Close()

	var outputFile *os.File
	outputFilePatch := fmt.Sprintf("uploads/" + fileId + ".merged")
	if chunkIndex == "0" {
		// have to do this, because if you use os.open or os.create, it will just readonly
		outputFile, err = os.OpenFile(outputFilePatch, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
		if err != nil {
			return map[string]interface{}{
				"response": err.Error(),
			}
		}
	} else {
		outputFile, err = os.OpenFile(outputFilePatch, os.O_WRONLY|os.O_APPEND, 0644)
		if err != nil {
			return map[string]interface{}{
				"response": err.Error(),
			}
		}
	}
	defer outputFile.Close()

	_, err = io.Copy(outputFile, tempFile)
	if err != nil {
		fmt.Println("err copy:", err)
	}
	os.Remove(temporaryPath)
	if chunkIndex == lastChunkIndex {
		// i don't know why i cannot use outputfile above, i need to open it agait with different variable name
		outputFile2, err := os.OpenFile(outputFilePatch, os.O_RDWR|os.O_APPEND, 0644)
		if err != nil {
			return map[string]interface{}{
				"response": err.Error(),
			}
		}
		defer outputFile2.Close()

		buffer := make([]byte, 512)
		outputFile.Seek(0, io.SeekStart)
		_, err = outputFile2.Read(buffer)
		if err != nil {
			fmt.Println("err read:", err)
			return map[string]interface{}{
				"response": err.Error(),
			}
		}
		mimeType := http.DetectContentType(buffer)
		extention := ".bin"
		extentions, err := mime.ExtensionsByType(mimeType)
		fmt.Println("extentions:", extentions)
		if err != nil {
			return map[string]interface{}{
				"response": err.Error(),
			}
		}
		if len(extentions) > 0 {
			extention = extentions[1]
		}
		// you can check the extention file here

		finalPath := fmt.Sprintf("uploads/%s%s", fileId, extention)
		err = os.Rename(outputFilePatch, finalPath)
		if err != nil {
			return map[string]interface{}{
				"response": err.Error(),
			}
		}
		return map[string]interface{}{
			"response": "success",
		}
	}
	return map[string]interface{}{
		"chungIndex": chunkIndex,
	}
}
