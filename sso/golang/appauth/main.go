package main

import (
	"embed"
	"fmt"
	"html/template"
	"io"
	"net/http"

	"github.com/labstack/echo/v4"
)

//go:embed static/*
var embeddedFiles embed.FS
var appauthtoken = "appauthtoken"
var authorizationCode = "authorizationCode"
var clientId = "clientId"
var clientSecret = "clientSecret"
var redirectUri = "http://localhost:8081/callback"
var refreshToken = "apponerefreshtoken"
var oauthRedirect = "/oauth/authorize"

// TemplateRenderer implements echo.Renderer
type TemplateRenderer struct {
	templates *template.Template
}

func (t *TemplateRenderer) Render(w io.Writer, name string, data any, c echo.Context) error {
	return t.templates.ExecuteTemplate(w, name, data)
}

type TokenRequest struct {
	GrantType    string `form:"grant_type"`
	Code         string `form:"code"`
	RedirectURI  string `form:"redirect_uri"`
	ClientID     string `form:"client_id"`
	ClientSecret string `form:"client_secret"`
	RefreshToken string `form:"refresh_token"`
	State        string `form:"state"`
}

func main() {
	e := echo.New()

	e.Renderer = &TemplateRenderer{
		// templates: template.Must(template.ParseFS(embeddedFiles, "static/**/*.html")),
		templates: template.Must(template.New("").ParseGlob("static/*.html")),
	}

	e.POST("/login", func(c echo.Context) error {
		type LoginRequest struct {
			Email    string `form:"email" json:"email"`
			Password string `form:"password" json:"password"`
		}

		var loginRequest LoginRequest
		if err := c.Bind(&loginRequest); err != nil {
			data := map[string]any{
				"message": err.Error(),
			}
			return c.Render(http.StatusBadRequest, "authorize", data)
		}

		if loginRequest.Email == "" || loginRequest.Password == "" {
			data := map[string]any{
				"message": "email and password are required",
			}
			return c.Render(http.StatusBadRequest, "authorize", data)
		}

		if loginRequest.Email != "test@example.com" || loginRequest.Password != "password" {
			data := map[string]any{
				"message": "invalid email or password",
			}
			return c.Render(http.StatusUnauthorized, "authorize", data)
		}

		// set cookie with samesite none
		c.SetCookie(&http.Cookie{
			Name:     "appauthsessiontoken",
			Value:    "appauthsessiontoken",
			SameSite: http.SameSiteNoneMode,
			Secure:   true,
			HttpOnly: true,
		})
		return c.Redirect(http.StatusFound, oauthRedirect+"?client_id=")
	})

	e.GET("/authorize", func(c echo.Context) error {
		clientId := c.QueryParam("clientId")
		state := c.QueryParam("state")
		data := map[string]any{
			"clientId": clientId,
			"state":    state,
		}
		return c.Render(http.StatusOK, "authorize", data)
	})

	e.POST("/token", func(c echo.Context) error {
		var tokenRequest TokenRequest
		if err := c.Bind(&tokenRequest); err != nil {
			return c.JSON(http.StatusBadRequest, map[string]any{
				"error": "invalid request",
			})
		}

		switch tokenRequest.GrantType {
		case "authorization_code":
			return tokenFromAuthCode(c, tokenRequest)
		case "client_credentials":
			return tokenFromClientCrendentials(c, tokenRequest)
		case "refresh_token":
			return tokenFromRefreshToken(c, tokenRequest)
		default:
			return c.JSON(http.StatusBadRequest, map[string]string{
				"error": "invalid grant type",
			})
		}
	})

	e.Logger.Fatal(e.Start(":8080"))
}

func tokenFromAuthCode(c echo.Context, req TokenRequest) error {
	fmt.Println("authorization_code")
	// if req.Code == "" || req.Code != authorizationCode || req.ClientID != clientId || req.ClientSecret != clientSecret {
	if req.Code != authorizationCode || req.ClientID != clientId || req.ClientSecret != clientSecret {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "code is required",
		})
	}
	return c.JSON(http.StatusOK, map[string]string{
		"access_token":  "apponetoken",
		"refresh_token": "apponerefreshtoken",
		"expires_in":    "3600",
	})
}

func tokenFromClientCrendentials(c echo.Context, req TokenRequest) error {
	fmt.Println("client_credentials")
	if req.ClientID != clientId || req.ClientSecret != clientSecret {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "invalid request",
		})
	}
	return c.JSON(http.StatusOK, map[string]string{
		"access_token":  "apponetoken",
		"refresh_token": "apponerefreshtoken",
		"token_type":    "Bearer",
		"expires_in":    "3600",
	})
}

func tokenFromRefreshToken(c echo.Context, req TokenRequest) error {
	fmt.Println("refresh_token")
	if req.RefreshToken != refreshToken {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "invalid request",
		})
	}
	return c.JSON(http.StatusOK, map[string]string{
		"access_token":  "apponetoken",
		"refresh_token": "apponerefreshtoken",
		"expires_in":    "3600",
	})
}
