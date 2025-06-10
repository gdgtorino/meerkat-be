from pydantic import BaseModel


class TypeBox(BaseModel):
    id: int | None = None
    name: str