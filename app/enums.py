from enum import Enum


class TimedeltaKeyEnum(str, Enum):
    SECONDS = "seconds"
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"


class TimedeltaValueEnum(int, Enum):
    ONE = 1
    FIVE = 5
    TEN = 10
    FIFTEEN = 15
    TWENTY_FOUR = 24
    THIRTY = 30
    SIXTY = 60