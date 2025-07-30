use serde::Deserialize;
use validator::Validate;

#[derive(Debug, Deserialize, Validate)]
pub struct CreateRequest {
    #[validate(email(message = "invalid email format"), length(min = 1, max = 255, message = "email should has more then 1 and less then 255 characters"))]
    pub email: String,

    #[validate(length(min = 1, max = 32, message = "username should has more then 1 and less then 32 characters"))]
    pub username: String,

    #[validate(length(min = 1, max = 32, message = "phone number has should more then 1 and less then 32 characters"))]
    pub phone_number: String,

    #[
        validate(
            length(min = 1, max = 32, message = "password should has more then 1 and less then 32 characters"), 
            custom(function = "crate::helpers::validator_helper::validate_password")
        )
    ]
    pub password: String,
}