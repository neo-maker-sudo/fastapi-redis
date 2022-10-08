from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# https://fastapi.tiangolo.com/tutorial/sql-databases/#note
# check_same_thread is only for SQLite3, not need for other database
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)

# to have independent database session/connection per request, 
# use the same session through all the request and then close it after the request is finished.
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# use for create database models or classes ( orm models )
Base = declarative_base()

def retrieve_database():
    db = session_local()

    try:
        yield db

    finally:
        db.close()
