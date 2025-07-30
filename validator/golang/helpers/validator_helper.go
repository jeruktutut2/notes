package helpers

import (
	"net/http"
	"note-validator-golang/models/responses"
	"reflect"

	"github.com/go-playground/validator/v10"
)

func GetValidatorError(validatorError error, structRequest interface{}) (httpResponse responses.HttpResponse) {
	validationErrors := validatorError.(validator.ValidationErrors)
	val := reflect.ValueOf(structRequest)
	errorMessages := make(map[string]string)
	for _, fieldError := range validationErrors {
		structField, ok := val.Type().FieldByName(fieldError.Field())
		if !ok {
			errorMessages["property"] = "couldn't find property: " + fieldError.Field()
		}
		if fieldError.Tag() == "usernamevalidator" {
			errorMessages[structField.Tag.Get("json")] = "please use only uppercase and lowercase letter and number and min 5 and max 8 alphanumeric"
		} else if fieldError.Tag() == "passwordvalidator" {
			errorMessages[structField.Tag.Get("json")] = "please use only uppercase, lowercase, number and must have 1 uppercase. lowercase, number, @, _, -, min 8 and max 20"
		} else if fieldError.Tag() == "telephonevalidator" {
			errorMessages[structField.Tag.Get("json")] = "please use only number and + "
		} else if fieldError.Tag() == "email" {
			errorMessages[structField.Tag.Get("json")] = "please insert a correct email format"
		} else if fieldError.Tag() == "gte" {
			errorMessages[structField.Tag.Get("json")] = "please input greater than equal to " + fieldError.Param()
		} else {
			errorMessages[structField.Tag.Get("json")] = "is " + fieldError.Tag()
		}
	}
	httpResponse.HttpStatusCode = http.StatusBadRequest
	httpResponse.Response.Data = nil
	httpResponse.Response.Errors = errorMessages
	return
}
