package modelresponses

type SignResponse struct {
	Message   string `json:"message"`
	Signature string `json:"signature"`
}

func ToSignResponse(message string, signature string) SignResponse {
	return SignResponse{
		Message:   message,
		Signature: signature,
	}
}
