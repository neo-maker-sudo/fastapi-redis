from pydantic import BaseModel


class AccessTokenSchemaOut(BaseModel):
    access_token: str
    token_type: str