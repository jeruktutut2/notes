package main

import (
	"encoding/json"
	"fmt"
	"html/template"
	"io"
	"log"
	"net/http"
	"net/url"
	"strings"
	"time"

	"github.com/labstack/echo/v4"
)

var apponetoken = "apponetoken"

// TemplateRenderer implements echo.Renderer
type TemplateRenderer struct {
	templates *template.Template
}

func (t *TemplateRenderer) Render(w io.Writer, name string, data any, c echo.Context) error {
	return t.templates.ExecuteTemplate(w, name, data)
}

func main() {
	e := echo.New()

	// Load semua template
	renderer := &TemplateRenderer{
		templates: template.Must(template.ParseGlob("static/*.html")),
	}
	e.Renderer = renderer

	e.GET("/", func(c echo.Context) error {
		cookie, err := c.Cookie("appone")
		fmt.Println("cookie:", cookie)
		if err != nil {
			return c.Redirect(http.StatusFound, "http://localhost:8080/authorize?clientId=clientId&state=statexyz123")
		}
		if cookie.Value != apponetoken {
			return c.Redirect(http.StatusFound, "http://localhost:8080/authorize?clientId=clientId&state=statexyz123")
		}
		return c.Render(http.StatusOK, "home", nil)
	})

	e.GET("/callback", func(c echo.Context) error {
		code := c.QueryParam("code")
		state := "statexyz123"
		data := url.Values{}
		data.Set("grant_type", "authorization_code")
		data.Set("code", code)
		data.Set("redirect_uri", "http://localhost:8081")
		data.Set("client_id", "clientId")
		data.Set("client_secret", "clientSecret")
		data.Set("state", state)
		req, err := http.NewRequest(http.MethodPost, "http://localhost:8080/token", strings.NewReader(data.Encode()))
		if err != nil {
			return c.Render(http.StatusInternalServerError, "callback", nil)
		}
		req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
		client := &http.Client{}
		resp, err := client.Do(req)
		if err != nil {
			return c.Render(http.StatusInternalServerError, "callback", nil)
		}
		defer resp.Body.Close()

		if resp.StatusCode != http.StatusOK {
			return c.Render(http.StatusInternalServerError, "callback", nil)
		}
		var result map[string]any
		if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
			return c.Render(http.StatusInternalServerError, "callback", nil)
		}
		fmt.Println(result["access_token"].(string))
		c.SetCookie(&http.Cookie{
			Name:     "appone",
			Value:    result["access_token"].(string),
			Expires:  time.Now().Add(24 * time.Hour),
			Path:     "/",
			HttpOnly: true,
			Secure:   true,
			SameSite: http.SameSiteStrictMode,
		})
		return c.Redirect(http.StatusFound, "http://localhost:8081")
	})

	log.Fatalln(e.Start(":8081"))
}
