from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    username: str


class UserCreateSchema(UserBaseSchema):
    hashed_password: str


class UserBaseSchemaOut(UserBaseSchema):
    pass


class AccessTokenSchemaOut(BaseModel):
    access_token: str
    token_type: str