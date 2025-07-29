package modelresponses

import "net/http"

// type Error struct {
// 	Field   string `json:"field"`
// 	Message string `json:"message"`
// }

type BodyResponse struct {
	Data   interface{} `json:"data"`
	Errors interface{} `json:"errors"`
}

type MessageResponse struct {
	Message string `json:"message"`
}

type Response struct {
	HttpStatusCode int          `json:"httpStatusCode"`
	BodyResponse   BodyResponse `json:"response"`
}

func SetHttpResponse(httpStatusCode int, data interface{}, errors interface{}) Response {
	return Response{
		HttpStatusCode: httpStatusCode,
		BodyResponse: BodyResponse{
			Data:   data,
			Errors: errors,
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

func SetMessageHttpResponse(message string) Response {
	return Response{
		HttpStatusCode: http.StatusOK,
		BodyResponse: BodyResponse{
			Data: MessageResponse{
				Message: message,
			},
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
