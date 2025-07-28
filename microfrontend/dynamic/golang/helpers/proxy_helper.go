package helpers

import (
	"fmt"
	"net/http"
	"net/http/httputil"
	"net/url"

	"github.com/labstack/echo/v4"
)

func ProxyTo(target string, c echo.Context) error {
	url, err := url.Parse(target)
	if err != nil {
		fmt.Println("err: ", err)
		return err
	}
	proxy := httputil.NewSingleHostReverseProxy(url)
	proxy.ServeHTTP(c.Response(), c.Request())
	return nil
}

func ProxyWithPath(target string, targetPath string, c echo.Context) error {
	targetUrl, err := url.Parse(target)
	if err != nil {
		fmt.Println("err: ", err)
		return err
	}
	proxy := httputil.NewSingleHostReverseProxy(targetUrl)

	// Override path
	fmt.Println("targetUrl:", targetUrl)
	proxy.Director = func(req *http.Request) {
		req.URL.Scheme = targetUrl.Scheme
		req.URL.Host = targetUrl.Host
		req.URL.Path = targetPath
		req.Host = targetUrl.Host
	}
	proxy.ServeHTTP(c.Response(), c.Request())
	return nil
}
