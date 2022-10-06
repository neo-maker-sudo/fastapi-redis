import os
from redis_om import get_redis_connection
from dotenv import load_dotenv
from app.enums import TimedeltaKeyEnum, TimedeltaValueEnum

load_dotenv()

redis_db = get_redis_connection(
    host='localhost', port='6379'
)

class Settings:
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "")
    JWY_TOKEN_TYPE = "Bearer"
    ALGORITHM = "HS256"

    fake_db = {
        "neo": {
            "username": "neo"
        }
    }

    
    timedelta_seconds_args = {TimedeltaKeyEnum.SECONDS: TimedeltaValueEnum.FIVE}
    timedelta_minutes_args = {TimedeltaKeyEnum.MINUTES: TimedeltaValueEnum.THIRTY}

settings = Settings()