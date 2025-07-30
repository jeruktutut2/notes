package main

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/labstack/echo/v4"
)

type Signal struct {
	SDP  json.RawMessage `json:"sdp,omitempty"`
	Cand json.RawMessage `json:"candidate,omitempty"`
}

var (
	offerChan  = make(chan Signal)
	answerChan = make(chan Signal)
	callerIce  = make(chan Signal)
	calleeIce  = make(chan Signal)
)

func main() {
	e := echo.New()
	e.Static("/htmlcssjs", "static/htmlcssjs")
	e.Static("/nextjs", "static/nextjs")
	e.Static("/nuxtjs", "static/nuxtjs")

	// Calle receive Offer from caller
	e.POST("/offer", func(c echo.Context) error {
		fmt.Println("post /offer")
		var s Signal
		if err := c.Bind(&s); err != nil {
			return c.JSON(http.StatusInternalServerError, echo.Map{"data": nil, "errors": err})
		}
		fmt.Println("post offer signal:", s)
		offerChan <- s
		return c.NoContent(http.StatusOK)
	})

	// Callee gets Offer
	e.GET("/offer", func(c echo.Context) error {
		fmt.Println("get /offer")
		s := <-offerChan
		return c.JSON(http.StatusOK, s)
	})

	// Caller receive Answer from callee
	e.POST("/answer", func(c echo.Context) error {
		fmt.Println("post /answer")
		var s Signal
		if err := c.Bind(&s); err != nil {
			return c.JSON(http.StatusInternalServerError, echo.Map{"data": nil, "errors": err})
		}
		fmt.Println("post answer signal:", s)
		answerChan <- s
		return c.NoContent(http.StatusOK)
	})

	// Caller gets Answer
	e.GET("/answer", func(c echo.Context) error {
		fmt.Println("get /answer")
		s := <-answerChan
		return c.JSON(http.StatusOK, s)
	})

	// Caller sends ICE candidate
	e.POST("/caller-candidate", func(c echo.Context) error {
		fmt.Println("post /caller-candidate")
		var s Signal
		if err := c.Bind(&s); err != nil {
			return err
		}
		fmt.Println("post caller-candidate signal:", s)
		callerIce <- s
		return c.NoContent(http.StatusOK)
	})

	e.GET("/caller-candidate", func(c echo.Context) error {
		fmt.Println("get /caller-candidate")
		s := <-callerIce
		return c.JSON(http.StatusOK, s)
	})

	// Callee sends ICE candidate
	e.POST("/callee-candidate", func(c echo.Context) error {
		fmt.Println("post /callee-candidate")
		var s Signal
		if err := c.Bind(&s); err != nil {
			return err
		}
		fmt.Println("post callee-candidate signal:", s)
		calleeIce <- s
		return c.NoContent(http.StatusOK)
	})

	e.GET("/callee-candidate", func(c echo.Context) error {
		fmt.Println("get /callee-candidate")
		s := <-calleeIce
		return c.JSON(http.StatusOK, s)
	})

	e.Logger.Fatal(e.Start(":8080"))
}
