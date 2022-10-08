from fastapi import APIRouter, HTTPException, status, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.models.auth.schemas import (
    AccessTokenSchemaOut,
)
from app.config import settings
from app.database import retrieve_database
from app.utils.auth.jwt import encode_access_token, decode_access_token
from app.utils.user.password import verify_password
from app.utils.base.exceptions import (
    BadRequestError,
    NotFoundError,
    UnauthorizedError,
    credentials_exception,
)
from app.models.user.crud import create_user, retrieve_user_by_email
from app.models.user.schemas import UserCreateSchema, UserSchemaOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserSchemaOut)
def signup_view(user: UserCreateSchema, db: Session = Depends(retrieve_database)):
    try:
        if retrieve_user_by_email(db=db, email=user.email):
            raise BadRequestError

    except BadRequestError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )

    return create_user(db=db, user=user)


@router.post("/login", response_model=AccessTokenSchemaOut)
def login_view(email: EmailStr = Form(), password: str = Form(), db: Session = Depends(retrieve_database)):
    try:
        user = retrieve_user_by_email(db=db, email=email)
        
        if not user or not verify_password(password, user.password):
            raise BadRequestError

        access_token = encode_access_token(email)

    except BadRequestError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password",
        )

    except UnauthorizedError:
        raise credentials_exception

    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username or password"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server Error {e}",
        )

    return {"access_token": access_token, "token_type": settings.JWY_TOKEN_TYPE}


@router.get("/member", response_model=UserSchemaOut)
def member(user: str = Depends(decode_access_token)):
    return user
