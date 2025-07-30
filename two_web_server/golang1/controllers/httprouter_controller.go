package controllers

import (
	"encoding/json"
	"net/http"
	"time"

	"github.com/julienschmidt/httprouter"
)

type HttprouterController interface {
	LandingPage(w http.ResponseWriter, r *http.Request, ps httprouter.Params)
}

type httprouterController struct {
}

func NewHttprouterController() HttprouterController {
	return &httprouterController{}
}

func (controller *httprouterController) LandingPage(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	response := map[string]string{
		"app":  "httprouter",
		"time": time.Now().String(),
	}
	if err := json.NewEncoder(w).Encode(response); err != nil {
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
	}
}
