package modelresponses

type VerifyResponse struct {
	Message    string `json:"message"`
	Signature  string `json:"signature"`
	IsVerified bool   `json:"isVerified"`
}

func ToVerifyResponse(message string, signature string, isVerified bool) VerifyResponse {
	return VerifyResponse{
		Message:    message,
		Signature:  signature,
		IsVerified: isVerified,
	}
}
