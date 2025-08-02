from pydantic import BaseModel, model_validator, Field

class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    phone_number: str
    first_name: str
    last_name: str
    is_active: bool
    role: str

    class Config:
        from_attributes = True


class UserAuthData(BaseModel):
    username: str
    user_id: int
    user_role: str

class ChangePasswordSchema(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

    @model_validator(mode='after')
    def check_password_match(self) -> 'ChangePasswordSchema':
        if self.new_password != self.confirm_password:
            raise ValueError("New password and confirm password do not match")
        return self

class ChangePhoneSchema(BaseModel):
    new_phone: str = Field(min_length=8)