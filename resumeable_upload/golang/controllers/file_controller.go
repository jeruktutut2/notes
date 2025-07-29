package controllers

import (
	"fmt"
	"golang-note-resumeable-upload/services"
	"net/http"
	"strconv"

	"github.com/labstack/echo/v4"
)

type FileController interface {
	Upload(c echo.Context) error
	Merge(c echo.Context) error
	CheckFile(c echo.Context) error
	UploadAndMerge(c echo.Context) error
}

type fileController struct {
	fileService services.FileService
}

func NewFileController(fileService services.FileService) FileController {
	return &fileController{
		fileService: fileService,
	}
}

func (controller *fileController) Upload(c echo.Context) error {
	fileId := c.Request().Header.Get("X-File-Id")
	chunkIndex := c.Request().Header.Get("X-Chunk-Index")
	response := controller.fileService.Upload(c.Request().Context(), fileId, chunkIndex, c.Request().Body)
	return c.JSON(http.StatusOK, map[string]string{
		"response": response,
	})
}

func (controller *fileController) Merge(c echo.Context) error {
	fileId := c.Request().Header.Get("X-File-Id")
	totalChunksHeader := c.Request().Header.Get("X-Total-Chunks")
	totalChunks, err := strconv.Atoi(totalChunksHeader)
	if err != nil {
		return c.JSON(http.StatusOK, map[string]string{
			"response": err.Error(),
		})
	}
	response := controller.fileService.Merge(c.Request().Context(), fileId, totalChunks)
	fmt.Println("response:", response)
	return c.JSON(http.StatusOK, map[string]string{
		"response": response,
	})
}

func (controller *fileController) CheckFile(c echo.Context) error {
	fileId := c.Param("fileId")
	response, err := controller.fileService.CheckFile(c.Request().Context(), fileId)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"response": err.Error(),
		})
	}
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": response,
	})
}

func (controller *fileController) UploadAndMerge(c echo.Context) error {
	fileId := c.FormValue("fileId")
	chunkIndex := c.FormValue("chunkIndex")
	lastChunkIndex := c.FormValue("lastChunkIndex")
	fileHeader, err := c.FormFile("chunk")
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"response": err.Error(),
		})
	}
	file, err := fileHeader.Open()
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"response": err.Error(),
		})
	}
	defer file.Close()
	response := controller.fileService.UploadAndMerge(c.Request().Context(), fileId, chunkIndex, lastChunkIndex, file)
	return c.JSON(http.StatusOK, response)
}
