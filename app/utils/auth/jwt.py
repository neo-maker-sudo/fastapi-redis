from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer
from jose import JWTError, jwt
from app.config import settings
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
    expired_at = generate_jwt_expired_time(settings.timedelta_seconds_args)

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


def decode_access_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )

        username: str = payload.get("sub", None)

        if not username:
            raise credentials_exception
        
        if not settings.fake_db[username]:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception

    except Exception:
        raise Exception

    return settings.fake_db[username]