from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr


class UserCreateSchema(UserBaseSchema):
    password: str


class UserSchemaOut(UserBaseSchema):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
