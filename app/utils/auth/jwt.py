from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.config import settings
from app.models.user.crud import retrieve_user_by_email
from app.database import retrieve_database
from app.utils.base.exceptions import (
    UnauthorizedError,
    NotFoundError,
    credentials_exception,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def generate_jwt_expired_time(dt: dict):
    if not dt:
        dt = settings.timedelta_seconds_args

    return datetime.utcnow() + timedelta(**dt)


def generate_jwt_payload(data: str) -> dict:
    expired_at = generate_jwt_expired_time(settings.timedelta_minutes_args)

    if not data:
        raise NotFoundError

    return {
        "sub": data,
        "exp": expired_at if expired_at else None,
    }


def encode_access_token(data: str) -> str:
    try:
        payload = generate_jwt_payload(data)

        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
    
    except JWTError:
        raise UnauthorizedError

    except Exception as e:
        raise e


def decode_access_token(token: str = Depends(oauth2_scheme), db: Session = Depends(retrieve_database)):
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )

        email: str = payload.get("sub", None)

        if not email:
            raise credentials_exception
        
        user = retrieve_user_by_email(db=db, email=email)
        
        if not user:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception

    except Exception as e:
        raise e

    return user