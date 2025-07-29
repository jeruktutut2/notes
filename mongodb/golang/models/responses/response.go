package modelresponses

import "net/http"

type MessageResponse struct {
	Message string `json:"message"`
}

type BodyResponse struct {
	Data   interface{} `json:"data"`
	Errors interface{} `json:"errors"`
}

type Response struct {
	HttpStatusCode int
	BodyResponse   BodyResponse
}

func SetResponse(httpStatusCode int, data interface{}, errors interface{}) Response {
	return Response{
		HttpStatusCode: httpStatusCode,
		BodyResponse: BodyResponse{
			Data:   data,
			Errors: errors,
		},
	}
}

func SetDataResponse(httpStatusCode int, data interface{}) Response {
	return Response{
		HttpStatusCode: httpStatusCode,
		BodyResponse: BodyResponse{
			Data:   data,
			Errors: nil,
		},
	}
}

func SetMessageResponse(httpStatusCode int, message string) Response {
	return Response{
		HttpStatusCode: httpStatusCode,
		BodyResponse: BodyResponse{
			Data: MessageResponse{
				Message: message,
			},
			Errors: nil,
		},
	}
}

func SetOkResponse(data interface{}) Response {
	return Response{
		HttpStatusCode: http.StatusOK,
		BodyResponse: BodyResponse{
			Data:   data,
			Errors: nil,
		},
	}
}

func SetCreatedResponse(data interface{}) Response {
	return Response{
		HttpStatusCode: http.StatusCreated,
		BodyResponse: BodyResponse{
			Data:   data,
			Errors: nil,
		},
	}
}

func SetNoContentResponse() Response {
	return Response{
		HttpStatusCode: http.StatusNoContent,
		BodyResponse: BodyResponse{
			Data:   nil,
			Errors: nil,
		},
	}
}

func SetBadRequestResponse(message string) Response {
	return Response{
		HttpStatusCode: http.StatusBadRequest,
		BodyResponse: BodyResponse{
			Data: nil,
			Errors: MessageResponse{
				Message: message,
			},
		},
	}
}

func SetNotFoundResponse(message string) Response {
	return Response{
		HttpStatusCode: http.StatusNotFound,
		BodyResponse: BodyResponse{
			Data: nil,
			Errors: MessageResponse{
				Message: message,
			},
		},
	}
}

func SetUnauthorizedResponse(message string) Response {
	return Response{
		HttpStatusCode: http.StatusUnauthorized,
		BodyResponse: BodyResponse{
			Data: nil,
			Errors: MessageResponse{
				Message: message,
			},
		},
	}
}

func SetUserCloseHttpConnectionErrorResponse() Response {
	return Response{
		HttpStatusCode: 499,
		BodyResponse: BodyResponse{
			Data: nil,
			Errors: MessageResponse{
				Message: "user close http connection or cancel http connection",
			},
		},
	}
}

func SetTimeoutErrorResponse() Response {
	return Response{
		HttpStatusCode: http.StatusRequestTimeout,
		BodyResponse: BodyResponse{
			Data: nil,
			Errors: MessageResponse{
				Message: "request timeout",
			},
		},
	}
}

func SetRefreshTokenExpiredResponse() Response {
	return Response{
		HttpStatusCode: 498,
		BodyResponse: BodyResponse{
			Data: nil,
			Errors: MessageResponse{
				Message: "refresh token has expired",
			},
		},
	}
}

func SetInternalServerErrorResponse() Response {
	return Response{
		HttpStatusCode: http.StatusInternalServerError,
		BodyResponse: BodyResponse{
			Data: nil,
			Errors: MessageResponse{
				Message: "internal server error",
			},
		},
	}
}
