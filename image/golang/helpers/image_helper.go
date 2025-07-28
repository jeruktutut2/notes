package helpers

import (
	"bytes"
	"encoding/base64"
	"fmt"
	"image"
	_ "image/gif"
	_ "image/jpeg"
	_ "image/png"
	"io"
	"mime/multipart"
	"regexp"
	"strings"
)

type ImageHelper interface {
	ValidateFromBase64(file string) (err error)
	ValidateFromMultipartFile(file multipart.File) (err error)
}

type imageHelper struct {
}

func NewImageHelper() ImageHelper {
	return &imageHelper{}
}

func (helper *imageHelper) ValidateFromBase64(file string) (err error) {
	if strings.HasPrefix(file, "data:image/") {
		re := regexp.MustCompile(`^data:image\/[a-zA-Z]+;base64,`)
		file = re.ReplaceAllString(file, "")
	}

	decoded, err := base64.StdEncoding.DecodeString(file)
	if err != nil {
		return
	}

	// mimeType := http.DetectContentType(decoded[:512])
	// fmt.Println("mimeType:", mimeType)
	// if mimeType != "image/jpeg" && mimeType != "image/png" {
	// 	return
	// }

	_, format, err := image.Decode(bytes.NewReader(decoded))
	fmt.Println("format:", format)
	if err != nil {
		return
	}
	return
}

func (helper *imageHelper) ValidateFromMultipartFile(file multipart.File) (err error) {
	// sourceFile, err := fileHeader.Open()
	// if err != nil {
	// 	return
	// }
	// defer sourceFile.Close()

	var buf bytes.Buffer
	tee := io.TeeReader(file, &buf)

	magic := make([]byte, 512)
	_, err = tee.Read(magic)
	if err != nil && err != io.EOF {
		return
	}

	// mimeType := http.DetectContentType(magic)
	// fmt.Println("mimeType:", mimeType)
	// if mimeType != "image/jpeg" && mimeType != "image/png" {
	// 	return
	// }

	_, format, err := image.Decode(&buf)
	fmt.Println("format:", format)
	if err != nil {
		return
	}
	return
}
