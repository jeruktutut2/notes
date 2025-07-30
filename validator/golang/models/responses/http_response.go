package responses

type Response struct {
	Data   interface{} `json:"data"`
	Errors interface{} `json:"errors"`
}

type HttpResponse struct {
	HttpStatusCode int      `json:"httpStatusCode"`
	Response       Response `json:"response"`
}

func SetDataHttpResponse(httpStatusCode int, data interface{}) HttpResponse {
	return HttpResponse{
		HttpStatusCode: httpStatusCode,
		Response: Response{
			Data:   data,
			Errors: nil,
		},
	}
}
