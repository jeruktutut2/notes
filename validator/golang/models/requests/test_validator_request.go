package requests

type TestValidatorRequest struct {
	Email    string `json:"email" validate:"required,email,min=1,max=10"`
	Username string `json:"username" validate:"required,min=8,max=50"`
	Password string `json:"password" validate:"required,passwordvalidator"`
}
