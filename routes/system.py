from fastapi import APIRouter

router = APIRouter(tags=["system"])


@router.get("/")
def hello() -> dict[str, str]:
    return {"message": "Hello, World!"}
