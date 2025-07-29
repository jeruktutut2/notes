package middlewares

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"strconv"
	"time"

	"note-request-response-log-golang/helpers"
	modelresponses "note-request-response-log-golang/models/responses"

	"github.com/labstack/echo/v4"
)

type responseBodyWriter struct {
	io.Writer
	http.ResponseWriter
	status int
}

func (w *responseBodyWriter) WriteHeader(statusCode int) {
	w.status = statusCode
	w.ResponseWriter.WriteHeader(statusCode)
}

func (w *responseBodyWriter) Write(b []byte) (int, error) {
	return w.Writer.Write(b)
}

func PrintRequestResponseLog(next echo.HandlerFunc) echo.HandlerFunc {
	return func(c echo.Context) error {
		datetimeNowRequest := time.Now()
		requestMethod := c.Request().Method
		var err error
		var httpResponse modelresponses.HttpResponse

		requestId := c.Request().Context().Value(RequestIdKey).(string)

		var requestBody string
		requestBody = `""`
		body, errJsonRequestBody := io.ReadAll(c.Request().Body)
		if errJsonRequestBody != nil {
			helpers.PrintLogToTerminal(errJsonRequestBody, requestId)
			httpResponse = modelresponses.SetInternalServerErrorHttpResponse()
			err = errJsonRequestBody
		}
		if len(body) == 0 {
			errLenBody := errors.New("json len body equal to 0")
			helpers.PrintLogToTerminal(errLenBody, requestId)
			err = errLenBody
			httpResponse = modelresponses.SetInternalServerErrorHttpResponse()
		}
		jsonRequestBodyMap := make(map[string]interface{})
		errJsonRequestBodyMap := json.Unmarshal(body, &jsonRequestBodyMap)
		if errJsonRequestBodyMap != nil {
			helpers.PrintLogToTerminal(errJsonRequestBodyMap, requestId)
			err = errJsonRequestBodyMap
			httpResponse = modelresponses.SetInternalServerErrorHttpResponse()
		}
		c.Request().Body = io.NopCloser(bytes.NewBuffer(body))

		if jsonRequestBodyMap != nil {
			if c.Request().URL.Path == "/api/v1/users/register" {
				delete(jsonRequestBodyMap, "password")
				delete(jsonRequestBodyMap, "confirmpassword")
			} else if c.Request().URL.Path == "/api/v1/users/login" {
				delete(jsonRequestBodyMap, "password")
			}

			jsonRequestBodyByte, errJsonRequestBodyByte := json.Marshal(jsonRequestBodyMap)
			if errJsonRequestBodyByte != nil {
				helpers.PrintLogToTerminal(errJsonRequestBodyByte, requestId)
				httpResponse = modelresponses.SetInternalServerErrorHttpResponse()
				err = errJsonRequestBodyByte
			}
			requestBody = string(jsonRequestBodyByte)
		}

		host := c.Request().Host
		protocol := ""
		if c.Request().TLS == nil {
			protocol = "http"
		} else {
			protocol = "https"
		}
		urlPath := c.Request().URL.Path
		userAgent := c.Request().Header.Get("User-Agent")
		remoteAddr := c.Request().RemoteAddr
		forwardedFor := c.Request().Header.Get("X-Forwarded-For")

		requestLog := `{"requestTime": "` + datetimeNowRequest.String() + `", "app": "project-backend", "method": "` + requestMethod + `","requestId":"` + requestId + `","host": "` + host + `","urlPath":"` + urlPath + `","protocol":"` + protocol + `","body": ` + requestBody + `, "userAgent": "` + userAgent + `", "remoteAddr": "` + remoteAddr + `", "forwardedFor": "` + forwardedFor + `"}`
		fmt.Println(requestLog)
		if err != nil {
			return c.JSON(httpResponse.HttpStatusCode, httpResponse.Response)
		}

		// so i can catch the response body
		resBody := new(bytes.Buffer)
		mw := io.MultiWriter(c.Response().Writer, resBody)
		writer := &responseBodyWriter{
			Writer:         mw,
			ResponseWriter: c.Response().Writer,
		}
		c.Response().Writer = writer

		err = next(c)
		if err != nil {
			c.Error(err)
		}

		responseBody := resBody.String()
		responseStatus := writer.status
		log := `{"responseTime": "` + time.Now().String() + `", "app": "project-backend", "requestId": "` + requestId + `", "responseStatus": ` + strconv.Itoa(responseStatus) + `, "response": ` + responseBody + `}`
		fmt.Println(log)
		return nil
	}
}

func PrintRequestResponseLogWithNoRequestBody(next echo.HandlerFunc) echo.HandlerFunc {
	return func(c echo.Context) error {
		datetimeNowRequest := time.Now()
		requestMethod := c.Request().Method
		var err error
		requestId := c.Request().Context().Value(RequestIdKey).(string)

		requestBody := `""`

		host := c.Request().Host
		protocol := ""
		if c.Request().TLS == nil {
			protocol = "http"
		} else {
			protocol = "https"
		}
		urlPath := c.Request().URL.Path
		userAgent := c.Request().Header.Get("User-Agent")
		remoteAddr := c.Request().RemoteAddr
		forwardedFor := c.Request().Header.Get("X-Forwarded-For")

		requestLog := `{"requestTime": "` + datetimeNowRequest.String() + `", "app": "project-backend", "method": "` + requestMethod + `","requestId":"` + requestId + `","host": "` + host + `","urlPath":"` + urlPath + `","protocol":"` + protocol + `","body": ` + requestBody + `, "userAgent": "` + userAgent + `", "remoteAddr": "` + remoteAddr + `", "forwardedFor": "` + forwardedFor + `"}`
		fmt.Println(requestLog)

		// so i can catch the response body
		resBody := new(bytes.Buffer)
		mw := io.MultiWriter(c.Response().Writer, resBody)
		writer := &responseBodyWriter{Writer: mw, ResponseWriter: c.Response().Writer}
		c.Response().Writer = writer

		err = next(c)
		if err != nil {
			c.Error(err)
		}

		responseBody := resBody.String()
		log := `{"responseTime": "` + time.Now().String() + `", "app": "project-backend", "requestId": "` + requestId + `", "response": ` + responseBody + `}`
		fmt.Println(log)
		return nil
	}
}
