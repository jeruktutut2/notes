package main

import (
	"context"
	"image-note-golang/helpers"
	"net/http"
	"os"
	"os/signal"
	"time"

	"github.com/labstack/echo/v4"
)

type Request struct {
	Image string `json:"image"`
}

func main() {
	imageHelper := helpers.NewImageHelper()
	e := echo.New()
	e.GET("/image", func(c echo.Context) error {
		var request Request
		err := c.Bind(&request)
		if err != nil {
			return c.JSON(http.StatusBadRequest, echo.Map{
				"response": err.Error(),
			})
		}
		err = imageHelper.ValidateFromBase64(request.Image)
		if err != nil {
			return c.JSON(http.StatusInternalServerError, echo.Map{
				"response": err.Error(),
			})
		}
		return c.File("images/image.jpg")
	})
	e.POST("/image", func(c echo.Context) error {
		fileHeader, err := c.FormFile("image")
		if err != nil {
			return c.JSON(http.StatusInternalServerError, echo.Map{
				"response": err.Error(),
			})
		}
		sourceFile, err := fileHeader.Open()
		if err != nil {
			return c.JSON(http.StatusInternalServerError, echo.Map{
				"response": err.Error(),
			})
		}
		defer sourceFile.Close()

		// buf := new(bytes.Buffer)
		// _, err = io.Copy(buf, sourceFile)
		// if err != nil {
		// 	return c.JSON(http.StatusInternalServerError, echo.Map{
		// 		"response": err.Error(),
		// 	})
		// }
		// bytes.NewReader(buf.Bytes())
		err = imageHelper.ValidateFromMultipartFile(sourceFile)
		if err != nil {
			return c.JSON(http.StatusInternalServerError, echo.Map{
				"response": err.Error(),
			})
		}
		return c.JSON(http.StatusOK, echo.Map{
			"response": "ok",
		})
	})

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
	defer stop()
	go func() {
		if err := e.Start(":8080"); err != nil && err != http.ErrServerClosed {
			e.Logger.Fatal("shutting down the server")
		}
	}()

	<-ctx.Done()
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := e.Shutdown(ctx); err != nil {
		e.Logger.Fatal(err)
	}
}
