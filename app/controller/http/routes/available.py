from fastapi import APIRouter

router = APIRouter(prefix="")


@router.get("/")
async def available():
    return {"status": "success"}
