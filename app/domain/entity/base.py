from pydantic import BaseModel


class ListDTO(BaseModel):
    """Pagination model template"""
    page: int
    has_next: bool
    list: list


class FilterDTO(BaseModel):
    """Filter template"""
    page: int = 1
