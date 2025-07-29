package services

import (
	"fmt"
	"io"
	"net/http"
	"os"
)

type FileService interface {
	GetFileStat() (httpStatusCode int, response map[string]interface{})
	Download(w http.ResponseWriter, rangeHeader string) (httpStatusCode int, response map[string]interface{})
}

type fileService struct {
}

func NewFileService() FileService {
	return &fileService{}
}

func (service *fileService) GetFileStat() (httpStatusCode int, response map[string]interface{}) {
	var err error
	filepath := "uploads/file_upload.mp4"
	fileStat, err := os.Stat(filepath)
	if err != nil {
		return http.StatusInternalServerError, map[string]interface{}{
			"response": err.Error(),
		}
	}
	return http.StatusOK, map[string]interface{}{
		"filename": "file_upload.mp4",
		"size":     fileStat.Size(),
	}
}

func (service *fileService) Download(w http.ResponseWriter, rangeHeader string) (httpStatusCode int, response map[string]interface{}) {
	var err error
	filepath := "uploads/file_upload.mp4"
	file, err := os.Open(filepath)
	if err != nil {
		return http.StatusInternalServerError, map[string]interface{}{
			"response": err.Error(),
		}
	}
	defer file.Close()

	fileStat, err := file.Stat()
	if err != nil {
		return http.StatusInternalServerError, map[string]interface{}{
			"response": err.Error(),
		}
	}

	startByte := int64(0)
	endByte := int64(0)
	if rangeHeader != "" {
		_, err = fmt.Sscanf(rangeHeader, "bytes=%d-%d", &startByte, &endByte)
		if err != nil {
			return http.StatusInternalServerError, map[string]interface{}{
				"response": err.Error(),
			}
		}
	}

	length := endByte - startByte + 1
	_, err = file.Seek(startByte, io.SeekStart)
	if err != nil {
		return http.StatusInternalServerError, map[string]interface{}{
			"response": err.Error(),
		}
	}

	w.Header().Set("Content-Type", "application/octet-stream")
	w.Header().Set("Content-Range", fmt.Sprintf("bytes %d-%d/%d", startByte, fileStat.Size()-1, fileStat.Size()))
	w.Header().Set("Content-Length", fmt.Sprintf("%d", length))
	w.Header().Set("Accept-Ranges", "bytes")
	w.WriteHeader(http.StatusPartialContent)

	_, err = io.CopyN(w, file, length)
	if err != nil {
		return http.StatusInternalServerError, map[string]interface{}{
			"response": err.Error(),
		}
	}

	return http.StatusOK, map[string]interface{}{
		"response": "ok",
	}
}
