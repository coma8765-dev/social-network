from fastapi import APIRouter, Depends

from app.domain.entity.posts import *
from app.domain.service.posts import PostService

router = APIRouter(tags=["posts"], prefix="/posts")


@router.post("/", status_code=201, response_model=Post)
async def create(
        ref: PostRef,
        use_case: PostService = Depends(),
):
    return await use_case.create(ref)


@router.get("/", response_model=PostList)
async def list_(
        params: PostFilter = Depends(PostFilter),
        use_case: PostService = Depends(),
):
    return await use_case.list(params)


@router.get("/{id_}/", response_model=Post)
async def get(
        id_: int,
        use_case: PostService = Depends(),
):
    return await use_case.get(id_)


@router.patch("/{id_}/", status_code=204)
async def update(
        id_: int,
        ref: PostUpdate,
        use_case: PostService = Depends(),
):
    await use_case.update(id_, ref)


@router.delete("/{id_}/", status_code=204)
async def delete(
        id_: int,
        use_case: PostService = Depends(),
):
    await use_case.delete(id_)


@router.post("/{id_}/estimate/", status_code=204)
async def estimate(
        id_: int,
        ref: PostEstimate = Depends(),
        use_case: PostService = Depends(),
):
    await use_case.estimate(id_, ref)
