package main

import (
	"context"
	"embed"
	"io/fs"
	"net/http"
	"os"
	"os/signal"
	"sync"
	"time"

	"github.com/go-webauthn/webauthn/protocol"
	"github.com/go-webauthn/webauthn/webauthn"
	"github.com/google/uuid"
	"github.com/labstack/echo/v4"
	"github.com/labstack/gommon/log"
)

//go:embed static/*
var embeddedFiles embed.FS

var wa *webauthn.WebAuthn

// var sessionData map[string]*webauthn.SessionData = make(map[string]*webauthn.SessionData)
var users map[string]*User = make(map[string]*User)
var usersLock sync.Mutex
var sessionDataStore map[string]*webauthn.SessionData = make(map[string]*webauthn.SessionData)

type User struct {
	ID          []byte
	Name        string
	DisplayName string
	Credentials []webauthn.Credential
}

func (u *User) WebAuthnID() []byte {
	return u.ID
}
func (u *User) WebAuthnName() string {
	return u.Name
}

func (u *User) WebAuthnDisplayName() string {
	return u.DisplayName
}

func (u *User) WebAuthnCredentials() []webauthn.Credential {
	return u.Credentials
}

type Register struct {
	Username string `json:"username"`
}

func main() {
	e := echo.New()
	e.Logger.SetLevel(log.INFO)
	staticFiles, _ := fs.Sub(embeddedFiles, "static")
	e.POST("/register/begin", registerBegin)
	e.GET("/*", echo.WrapHandler(http.FileServer(http.FS(staticFiles))))

	var err error
	wa, err = webauthn.New(&webauthn.Config{
		RPDisplayName: "localhost display name",
		RPID:          "localhost",
		RPOrigins:     []string{"localhost:8080"},
	})
	if err != nil {
		log.Fatal("err create new webauthn:", err)
	}

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
	defer stop()
	// Start server
	go func() {
		if err := e.Start(":8080"); err != nil && err != http.ErrServerClosed {
			e.Logger.Fatal("shutting down the server")
		}
	}()
	// Wait for interrupt signal to gracefully shut down the server with a timeout of 10 seconds.
	<-ctx.Done()
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := e.Shutdown(ctx); err != nil {
		e.Logger.Fatal(err)
	}
}

func registerBegin(c echo.Context) error {
	register := new(Register)
	err := c.Bind(register)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, echo.Map{
			"response": err.Error(),
		})
	}

	usersLock.Lock()
	defer usersLock.Unlock()
	user, ok := users[register.Username]
	if ok {
		return c.JSON(http.StatusForbidden, echo.Map{
			"response": "username: " + register.Username + " already exists",
		})
	}

	user = &User{
		ID:          []byte(uuid.NewString()),
		Name:        register.Username,
		DisplayName: register.Username,
		Credentials: []webauthn.Credential{},
	}
	users[register.Username] = user

	creation, sessionData, err := wa.BeginMediatedRegistration(
		user,
		protocol.MediationDefault,
		webauthn.WithResidentKeyRequirement(protocol.ResidentKeyRequirementRequired),
		webauthn.WithExclusions(webauthn.Credentials(user.WebAuthnCredentials()).CredentialDescriptors()),
		webauthn.WithExtensions(map[string]interface{}{"credProps": true}))

	// fmt.Println("user:", user)
	// fmt.Println("err:", err)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, echo.Map{
			"response": err.Error(),
		})
	}
	// fmt.Println("creation:", creation)
	// fmt.Println("sessionData:", sessionData)
	sessionDataStore["register"] = sessionData
	return c.JSON(http.StatusOK, echo.Map{
		"creation": creation,
	})
	// return nil
}

func registerFinish(c echo.Context) error {
	return nil
}
