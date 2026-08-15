package main

import (
	"context"
	"crypto/sha256"
	"encoding/base64"
	"html/template"
	"io"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/labstack/echo/v5"
	"github.com/labstack/echo/v5/middleware"
)

type TemplateRenderer struct {
	templates *template.Template
}

func (t *TemplateRenderer) Render(c *echo.Context, w io.Writer, name string, data any) error {
	return t.templates.ExecuteTemplate(w, name, data)
}

type Client struct {
	ClientId            string
	ClientSecret        string
	Username            string
	Password            string
	RedirectURI         string
	Cookie              string
	Code                string
	CodeChallange       string
	CodeChallengeMethod string
}

var clients = map[string]Client{
	"client1": {
		ClientId:     "client1",
		ClientSecret: "secret1",
		Username:     "user1",
		Password:     "pass1",
		// RedirectURI:         "http://localhost:8080/callback",
		RedirectURI:         "http://localhost:3000/callback",
		Cookie:              "appauthlogincookie",
		CodeChallange:       "",
		CodeChallengeMethod: "",
	},
}

func main() {
	e := echo.New()
	e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
		AllowOrigins: []string{"https://labstack.com", "https://labstack.net", "http://localhost:3000"},
		AllowHeaders: []string{echo.HeaderOrigin, echo.HeaderContentType, echo.HeaderAccept},
	}))
	e.Renderer = &TemplateRenderer{
		// templates: template.Must(template.New("").ParseGlob("static/*.html")),
		templates: template.Must(template.New("").ParseGlob("views/*.html")),
	}
	e.GET("/", func(c *echo.Context) error {
		return c.String(200, "Hello, World!")
	})
	// ?response_type=code&client_id=client1&code_challange=code_challange&code_challenge_method=code_challenge_method
	// e.POST("/oauth/authorize", func(c *echo.Context) error {
	e.GET("/oauth/authorize", func(c *echo.Context) error {
		responseType := c.QueryParam("response_type")
		clientid := c.QueryParam("client_id")

		client := clients[clientid]
		client.CodeChallange = c.QueryParam("code_challange")
		client.CodeChallengeMethod = c.QueryParam("code_challenge_method")
		clients[clientid] = client

		cookie, err := c.Cookie("appauthlogincookie")
		// fmt.Println(err == nil, err == http.ErrNoCookie, cookie.Value != clients[clientid].Cookie)
		if err != nil && err != http.ErrNoCookie {
			return c.Render(500, "authorize", map[string]string{
				"error": "Internal server error",
			})
			// } else if err != nil || err == http.ErrNoCookie || cookie.Value != clients[clientid].Cookie {
			// } else if cookie.Value != clients[clientid].Cookie {
		} else if err == http.ErrNoCookie || cookie.Value != client.Cookie {
			// return c.Redirect(http.StatusFound, "http://localhost:8080/login?response_type="+responseType+"&clientid="+clientid+"&codechallange="+clients[clientid].CodeChallange+"&codechallengemethod="+clients[clientid].CodeChallengeMethod)
			return c.Redirect(http.StatusFound, "http://localhost:8080/login?response_type="+responseType+"&client_id="+clientid)
		}
		codeForToken := "code_for_token"
		client.Code = codeForToken
		clients[clientid] = client
		// return nil
		return c.Redirect(http.StatusFound, client.RedirectURI+"?code="+client.Code)
	})
	e.GET("/login", func(c *echo.Context) error {
		responseType := c.QueryParam("response_type")
		clientId := c.QueryParam("client_id")
		// codeChallange := c.QueryParam("code_challange")
		// codeChallengeMethod := c.QueryParam("code_challenge_method")
		// redirectURI := c.QueryParam("redirect_uri")
		// cookie, err := c.Cookie("appauthlogincookie")
		// if err != nil && err != http.ErrNoCookie {
		// 	return err
		// } else if err == nil && cookie.Value != "" {
		// 	return c.Redirect(http.StatusFound, "http://localhost:8080/authorize?")
		// }
		// redirectURI := c.QueryParam("redirect_uri")
		return c.Render(200, "login", map[string]string{
			"response_type": responseType,
			"client_id":     clientId,
			"username":      "",
			"password":      "",
			"message":       "",
			// "redirect_uri":  redirectURI,
		})
	})
	e.POST("/login", func(c *echo.Context) error {
		username := c.FormValue("username")
		password := c.FormValue("password")
		clientid := c.FormValue("client_id")
		responseType := c.FormValue("response_type")
		println("username:", username, clients[clientid].Username)
		println("password:", password, clients[clientid].Password)
		println("clientid:", clientid)
		println("responseType:", responseType)
		if username != clients[clientid].Username || password != clients[clientid].Password {
			return c.Render(400, "login", map[string]string{
				"response_type": responseType,
				"client_id":     clientid,
				"username":      username,
				"password":      password,
				"message":       "wrong username or password",
			})
		}
		// fmt.Println("mantap")
		c.SetCookie(&http.Cookie{
			Name:     "appauthlogincookie",
			Value:    clients[clientid].Cookie,
			Path:     "/",
			HttpOnly: true,
			Secure:   true,
			SameSite: http.SameSiteNoneMode,
			Expires:  time.Now().Add(24 * time.Hour),
		})
		// return nil
		return c.Redirect(http.StatusFound, "http://localhost:8080/oauth/authorize?response_type="+responseType+"&client_id="+clientid)
	})
	e.POST("/oauth/token", func(c *echo.Context) error {
		responseType := c.QueryParam("response_type")
		clientId := c.QueryParam("client_id")
		code := c.QueryParam("code")
		codeVerifier := c.QueryParam("code_verifier")
		if code != clients[clientId].Code {
			return c.Redirect(http.StatusFound, "http://localhost:8080/login?response_type="+responseType+"&client_id="+clientId)
		}

		sum := sha256.Sum256([]byte(codeVerifier))
		expected := base64.RawURLEncoding.EncodeToString(sum[:])
		println("codeVerifier:", codeVerifier)
		println("mantap:", clients[clientId].CodeChallange, expected)
		println("clients[clientId].CodeChallange != expected:", clients[clientId].CodeChallange != expected)
		if clients[clientId].CodeChallange != expected {
			return c.Redirect(http.StatusFound, "http://localhost:8080/login?response_type="+responseType+"&client_id="+clientId)
		}

		c.SetCookie(&http.Cookie{
			Name:     "apponetokencookie",
			Value:    "apponetokencookie",
			HttpOnly: true,
			Secure:   true,
			Expires:  time.Now().Add(24 * time.Hour),
			SameSite: http.SameSiteStrictMode,
		})
		return c.JSON(http.StatusOK, map[string]string{
			"message": "success",
		})
	})
	// e.Start(":8080")

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()
	sc := echo.StartConfig{
		// Address:         ":1323",
		Address:         ":8080",
		GracefulTimeout: 5 * time.Second,
	}
	if err := sc.Start(ctx, e); err != nil {
		e.Logger.Error("failed to start server", "error", err)
	}
}
