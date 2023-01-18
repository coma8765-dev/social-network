from pydantic import BaseModel, Field, constr


class HTTPException(BaseModel):
    detail: str | dict | list | int = constr()

    class Config:
        schema_extra = {
            "example": {
                "detail": "Some error",
            }
        }

