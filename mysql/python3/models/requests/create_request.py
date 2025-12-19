from pydantic import BaseModel, EmailStr, validator, ValidationError

class CreateRequest(BaseModel):
    test: str