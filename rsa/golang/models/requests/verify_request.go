package modelrequests

type VerifyRequest struct {
	Message   string `json:"message"`
	Signature string `json:"signature"`
}
