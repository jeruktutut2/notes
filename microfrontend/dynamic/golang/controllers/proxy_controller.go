package controllers

import (
	"fmt"
	"gateway/helpers"
	"net/http"
	"time"

	"github.com/labstack/echo/v4"
)

type ProxyController interface {
	SetRemote1Cookie(c echo.Context) error
	SetRemote2Cookie(c echo.Context) error
	RemoteEntry(c echo.Context) error
	Bundle(c echo.Context) error
	NotRemoteEntry(c echo.Context) error
}

type proxyController struct {
}

func NewProxyController() ProxyController {
	return &proxyController{}
}

func (controller *proxyController) SetRemote1Cookie(c echo.Context) error {
	fmt.Println("SetRemote1Cookie")
	cookie := new(http.Cookie)
	cookie.Name = "remote"
	cookie.Value = "remote1"
	cookie.Path = "/"
	cookie.Expires = time.Now().Add(24 * time.Hour)
	// cookie.HttpOnly = true
	// cookie.Secure = true
	c.SetCookie(cookie)
	return c.JSON(http.StatusOK, echo.Map{"response": "ok remote 1"})
}

func (controller *proxyController) SetRemote2Cookie(c echo.Context) error {
	fmt.Println("SetRemote2Cookie")
	cookie := new(http.Cookie)
	cookie.Name = "remote"
	cookie.Value = "remote2"
	cookie.Path = "/"
	cookie.Expires = time.Now().Add(24 * time.Hour)
	// cookie.HttpOnly = true
	// cookie.Secure = true
	c.SetCookie(cookie)
	return c.JSON(http.StatusOK, echo.Map{"response": "ok remote 2"})
}

func (controller *proxyController) RemoteEntry(c echo.Context) error {
	fmt.Println("RemoteEntry")
	cookie, err := c.Cookie("remote")
	if err != nil {
		return c.JSON(http.StatusInternalServerError, echo.Map{"response": err.Error()})
	}
	fmt.Println("cookie.Value:", cookie.Value)
	if cookie.Value == "remote1" {
		return helpers.ProxyTo("http://localhost:3001", c)
	} else if cookie.Value == "remote2" {
		return helpers.ProxyTo("http://localhost:3002", c)
	} else {
		return c.JSON(http.StatusOK, echo.Map{"response": "no proxy"})
	}
}

func (controller *proxyController) Bundle(c echo.Context) error {
	fmt.Println("Bundle")
	cookie, err := c.Cookie("remote")
	if err != nil {
		return c.JSON(http.StatusInternalServerError, echo.Map{"response": err.Error()})
	}
	fmt.Println("cookie.Value:", cookie.Value)
	if cookie.Value == "remote1" {
		return helpers.ProxyTo("http://localhost:3001", c)
	} else if cookie.Value == "remote2" {
		return helpers.ProxyTo("http://localhost:3002", c)
	} else {
		return c.JSON(http.StatusOK, echo.Map{"response": "no proxy"})
	}
}

func (controller *proxyController) NotRemoteEntry(c echo.Context) error {
	fmt.Println("NotRemoteEntry")
	cookie, err := c.Cookie("remote")
	if err != nil {
		return c.JSON(http.StatusInternalServerError, echo.Map{"response": err.Error()})
	}
	if cookie.Value == "remote1" {
		return helpers.ProxyWithPath("http://localhost:3001", "/assets/remoteEntry.js", c)
	} else if cookie.Value == "remote2" {
		return helpers.ProxyWithPath("http://localhost:3002", "/assets/remoteEntry.js", c)
	} else {
		return c.JSON(http.StatusOK, echo.Map{"response": "no proxy"})
	}
}
