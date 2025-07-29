package services

import (
	"context"
	modelrequests "golang-rsa/models/requests"
	modelresponses "golang-rsa/models/responses"
	"golang-rsa/utils"
	"net/http"
)

type KeyService interface {
	Sign(ctx context.Context, signRequest modelrequests.SignRequest) (httpStatusCode int, response modelresponses.SignResponse)
	Verify(ctx context.Context, verifyRequest modelrequests.VerifyRequest) (httpStatusCode int, response modelresponses.VerifyResponse)
}

type keyService struct {
	keyUtil utils.KeyUtil
}

func NewKeyServcie(keyUtil utils.KeyUtil) KeyService {
	return &keyService{
		keyUtil: keyUtil,
	}
}

func (service *keyService) Sign(ctx context.Context, signRequest modelrequests.SignRequest) (httpStatusCode int, response modelresponses.SignResponse) {
	signature, err := service.keyUtil.Sign(signRequest.Message)
	if err != nil {
		httpStatusCode = http.StatusInternalServerError
		return
	}

	httpStatusCode = http.StatusOK
	// response = modelresponses.SignResponse{
	// 	Message:   signRequest.Message,
	// 	Signature: signature,
	// }
	response = modelresponses.ToSignResponse(signRequest.Message, signature)
	return
}

func (service *keyService) Verify(ctx context.Context, verifyRequest modelrequests.VerifyRequest) (httpStatusCode int, response modelresponses.VerifyResponse) {
	isVerify, err := service.keyUtil.Verify(verifyRequest.Message, verifyRequest.Signature)
	if err != nil {
		httpStatusCode = http.StatusInternalServerError
		return
	}
	httpStatusCode = http.StatusOK
	response = modelresponses.ToVerifyResponse(verifyRequest.Message, verifyRequest.Signature, isVerify)
	return
}
