from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreateSchema
from app.utils.user.password import hashing_password


def retrieve_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def retrieve_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def retrieve_users(db: Session):
    return db.query(User).all()


def create_user(db: Session, user: UserCreateSchema):
    hashed_password = hashing_password(user.password)

    new_user = User(email=user.email, username=user.username, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
