from fastapi import APIRouter, HTTPException
from rsa import newkeys

from starlette import status

from app.api.deps import user_dependency, db_dependency
from app.core.security import bcrypt_context
from app.db.models import Users
from app.schemas.user_schema import ChangePasswordSchema, ChangePhoneSchema, UserSchema

router = APIRouter(prefix='/users', tags=['Users'])


@router.get("/me", status_code=status.HTTP_200_OK)
def get_user(user: user_dependency, db: db_dependency) -> UserSchema:
    user = db.query(Users).filter(Users.id == user.user_id).first()
    return UserSchema.model_validate(user)

@router.put("/me/password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(user: user_dependency, db: db_dependency, data: ChangePasswordSchema):
    user: Users = db.query(Users).filter(Users.id == user.user_id).first()

    if not bcrypt_context.verify(data.current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password do not match")

    if bcrypt_context.verify(data.new_password, user.hashed_password):
        raise HTTPException(status_code=400, detail='New password must be different than current password')

    user.hashed_password = bcrypt_context.hash(data.new_password)
    db.commit()
    db.refresh(user)


@router.patch("/me/phone", status_code=status.HTTP_200_OK, response_model=UserSchema)
def update_phone_number(user: user_dependency, db: db_dependency, data: ChangePhoneSchema) -> UserSchema:
    user: Users = db.query(Users).filter(Users.id == user.user_id).first()

    user.phone_number = data.new_phone
    db.commit()

    return UserSchema.model_validate(user)

