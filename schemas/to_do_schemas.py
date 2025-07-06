from pydantic import BaseModel
from typing import Optional

# Schema for creating a new todo (request)
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

# Schema for updating a todo (optional fields)
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# Schema for returning a todo (response)
class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool

    class Config:
        orm_mode = True
