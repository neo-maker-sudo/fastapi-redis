from fastapi import APIRouter

router = APIRouter(
    tags=["base"]
)


@router.get("/")
def root():
    return {"Hello": "World"}