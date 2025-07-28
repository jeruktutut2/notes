package modelresponses

import "net/http"

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

func SetMessageResponse(message string) Response {
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

func SetOkResponse(data interface{}) Response {
	return Response{
		HttpStatusCode: http.StatusOK,
		BodyResponse: BodyResponse{
			Data:   data,
			Errors: nil,
		},
	}
}

func SetCreateResponse(data interface{}) Response {
	return Response{
		HttpStatusCode: http.StatusOK,
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
