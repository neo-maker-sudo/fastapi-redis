from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.auth.schemas import (
    UserCreateSchema,
    AccessTokenSchemaOut,
)
from app.config import settings
from app.utils.auth.jwt import encode_access_token, decode_access_token
from app.utils.base.exceptions import (
    BadRequestError,
    NotFoundError,
    UnauthorizedError,
    credentials_exception
)


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/signup")
def signup_view():
    pass

@router.post("/login", response_model=AccessTokenSchemaOut)
def login_view(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        if not settings.fake_db.get(form_data.username, None):
            raise BadRequestError
        
        access_token = encode_access_token(form_data.username)
        
    except BadRequestError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password"
        )

    except UnauthorizedError:
        raise credentials_exception
    
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid username or password"
        )
   
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server Error {e}"
        )

    return {"access_token": access_token, "token_type": settings.JWY_TOKEN_TYPE}


@router.get("/member")
def member(username: str = Depends(decode_access_token)):
    return {"member": username}