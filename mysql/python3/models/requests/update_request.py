from pydantic import BaseModel

class UpdateRequest(BaseModel):
    id: int
    test: str