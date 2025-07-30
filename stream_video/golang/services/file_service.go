package services

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"strconv"
	"strings"
)

type FileService interface {
	Stream(w http.ResponseWriter, rangeHeader string) (httpStatusCode int, response map[string]interface{})
}

type fileService struct {
}

func NewFileService() FileService {
	return &fileService{}
}

func (service *fileService) Stream(w http.ResponseWriter, rangeHeader string) (httpStatusCode int, response map[string]interface{}) {
	var err error
	filepath := "videos/file_upload.mp4"
	file, err := os.Open(filepath)
	if err != nil {
		fmt.Println("open file:", err)
		return http.StatusInternalServerError, map[string]interface{}{
			"response": err.Error(),
		}
	}
	defer file.Close()

	fileStat, err := file.Stat()
	if err != nil {
		fmt.Println("file stat:", err)
		return http.StatusInternalServerError, map[string]interface{}{
			"response": err.Error(),
		}
	}

	if rangeHeader == "" {
		w.Header().Set("Content-Type", "video/mp4")
		w.Header().Set("Content-Length", fmt.Sprintf("%d", fileStat.Size()))
		_, err := io.Copy(w, file)
		if err != nil {
			fmt.Println("io copyn:", err)
			return http.StatusInternalServerError, map[string]interface{}{
				"response": err.Error(),
			}
		}
	}

	rangeParts := strings.Split(strings.Replace(rangeHeader, "bytes=", "", 1), "-")
	start, err := strconv.ParseInt(rangeParts[0], 10, 64)
	if err != nil {
		return http.StatusInternalServerError, map[string]interface{}{
			"response": err.Error(),
		}
	}
	end := fileStat.Size() - 1
	if len(rangeParts) > 1 && rangeParts[1] != "" {
		end, err = strconv.ParseInt(rangeParts[1], 10, 64)
		if err != nil {
			return http.StatusInternalServerError, map[string]interface{}{
				"response": err.Error(),
			}
		}
	}
	if end >= fileStat.Size() {
		end = fileStat.Size() - 1
	}

	length := end - start + 1
	_, err = file.Seek(start, io.SeekStart)
	if err != nil {
		fmt.Println("file seek:", err)
		return http.StatusInternalServerError, map[string]interface{}{
			"response": err.Error(),
		}
	}

	w.Header().Set("Content-Type", "video/mp4")
	w.Header().Set("Accept-Ranges", "bytes")
	w.Header().Set("Content-Range", fmt.Sprintf("bytes %d-%d/%d", start, end, fileStat.Size()))
	w.Header().Set("Content-Length", fmt.Sprintf("%d", length))
	w.WriteHeader(http.StatusPartialContent)

	_, err = io.CopyN(w, file, length)
	if err != nil {
		fmt.Println("io copyn:", err)
		return http.StatusInternalServerError, map[string]interface{}{
			"response": err.Error(),
		}
	}

	return http.StatusOK, map[string]interface{}{
		"response": "ok",
	}
}
