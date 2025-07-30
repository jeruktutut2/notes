package middlewares

import (
	"fmt"
	"net/http"

	"github.com/julienschmidt/httprouter"
)

func HttprouterExampleMiddleware(next httprouter.Handle) httprouter.Handle {
	return func(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
		fmt.Println(">> httprouter Middleware")
		next(w, r, ps)
	}
}

type Middleware func(httprouter.Handle) httprouter.Handle

func MultiMiddleware(h httprouter.Handle, middlewares ...Middleware) httprouter.Handle {
	for _, m := range middlewares {
		h = m(h)
	}
	return h
}
