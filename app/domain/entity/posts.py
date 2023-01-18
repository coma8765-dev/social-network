from datetime import datetime

from pydantic import BaseModel, Field, conlist, constr

from app.domain.entity.base import FilterDTO, ListDTO


class PostMetaRef(BaseModel):
    title: constr(max_length=200) = Field(description="Post's title")


class PostRef(PostMetaRef):
    body: constr(max_length=50000) = Field(description="Post's inner text")


class PostMeta(PostMetaRef):
    id: int = Field(description="Post ID")
    liked: bool | None = Field(description="User estimation")
    created_by: int = Field(description="ID of the user who created the post")
    create_date: datetime = Field(description="Create datetime")


class Post(PostMeta, PostRef):
    pass


class PostUpdate(BaseModel):
    title: constr(max_length=200) | None
    body: constr(max_length=50000) | None


class PostList(ListDTO):
    list: conlist(PostMeta, max_items=100)


class PostFilter(FilterDTO):
    title: constr(max_length=200) | None = None
    # keywords: conlist(constr(max_length=50), max_items=10)


class PostEstimate(BaseModel):
    positive: bool = True
    clear: bool = False
