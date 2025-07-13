from pydantic import BaseModel


class UserInDB(BaseModel):
    username: str
    user_id: int
    user_role: str