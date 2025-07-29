package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"sync"
	"time"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func main() {
	e := echo.New()
	e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
		AllowOrigins: []string{"http://localhost:3000", "*"},
		AllowHeaders: []string{echo.HeaderOrigin, echo.HeaderContentType, echo.HeaderAccept},
	}))
	e.GET("/stream/response", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]interface{}{
			"response": "response stream",
		})
	})
	e.GET("/stream/stream-with-channel", func(c echo.Context) error {
		c.Response().Header().Set(echo.HeaderContentType, echo.MIMETextHTMLCharsetUTF8)
		c.Response().WriteHeader(http.StatusOK)
		channelStream := make(chan string)
		service(channelStream)
		enc := json.NewEncoder(c.Response())
		for value := range channelStream {
			fmt.Println("value:", value)
			if err := enc.Encode(value); err != nil {
				return err
			}
			c.Response().Flush()
		}
		return c.String(http.StatusOK, "Hello, World! stream-with-channel")
	})

	e.GET("/stream/stream-without-channel", func(c echo.Context) error {
		fmt.Println("mantap")
		c.Response().Header().Set("Content-Type", "text/event-stream")
		c.Response().Header().Set("Cache-Control", "no-cache")
		c.Response().WriteHeader(http.StatusOK)
		serviceWithoutChannel(c)
		return c.JSON(http.StatusOK, map[string]interface{}{
			"response": "Hello, World! stream-without-channel",
		})
	})

	e.GET("/stream/stream-with-sse", func(c echo.Context) error {
		c.Response().Header().Set("Content-Type", "text/event-stream")
		c.Response().Header().Set("Cache-Control", "no-cache")
		c.Response().Header().Set("Connection", "keep-alive")
		serviceWithSSE(c)
		return c.String(http.StatusOK, "Hello, World! stream-with-sse")
	})
	e.Logger.Fatal(e.Start(":8080"))
}

func service(streamChannel chan string) {
	group := &sync.WaitGroup{}
	group.Add(1)
	go func() {
		defer group.Done()
		streamChannel <- "response 1\n\n"
		fmt.Println("streamChannel <- response 1")
		time.Sleep(2 * time.Second)

		streamChannel <- "response 2\n\n"
		fmt.Println("streamChannel <- response 2")
		time.Sleep(2 * time.Second)

		streamChannel <- "response 3\n\n"
		fmt.Println("streamChannel <- response 3")
		time.Sleep(2 * time.Second)

		streamChannel <- "response 4\n\n"
		fmt.Println("streamChannel <- response 4")
		time.Sleep(2 * time.Second)

		streamChannel <- "response 5\n\n"
		fmt.Println("streamChannel <- response 5")
		time.Sleep(2 * time.Second)
	}()
	go func() {
		group.Wait()
		close(streamChannel)
	}()
}

func serviceWithoutChannel(c echo.Context) {
	fmt.Println(1)
	var stream1 map[string]interface{}
	stream1 = map[string]interface{}{
		"response": "stream1",
	}
	json.NewEncoder(c.Response()).Encode(stream1)
	c.Response().Flush()
	time.Sleep(2 * time.Second)

	fmt.Println(2)
	var stream2 map[string]interface{}
	stream2 = map[string]interface{}{
		"response": "stream2",
	}
	json.NewEncoder(c.Response()).Encode(stream2)
	c.Response().Flush()
	time.Sleep(2 * time.Second)

	fmt.Println(3)
	var stream3 map[string]interface{}
	stream3 = map[string]interface{}{
		"response": "stream3",
	}
	json.NewEncoder(c.Response()).Encode(stream3)
	c.Response().Flush()
}

func serviceWithSSE(c echo.Context) {
	json.NewEncoder(c.Response()).Encode("stream1\n\n")
	c.Response().Flush()
	time.Sleep(2 * time.Second)
	json.NewEncoder(c.Response()).Encode("stream2\n\n")
	c.Response().Flush()
	time.Sleep(2 * time.Second)
	json.NewEncoder(c.Response()).Encode("stream3\n\n")
	c.Response().Flush()
}
