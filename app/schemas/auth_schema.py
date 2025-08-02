from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    message: str
    role: str

class CreateUserRequest(BaseModel):
    username: str
    email: str
    phone_number: str = Field(min_length=8)
    first_name: str
    last_name: str
    password: str
    role: str
