"""
Pydantic Schema
"""

from pydantic import BaseModel


class GetTaskSchemaResponse(BaseModel):
    """Get task response schema"""
    id: int
    title: str
    description: str
    completed: bool

    class Config:
        orm_mode = True

class TaskCreateRequest(BaseModel):
    """post task request schema"""
    title: str
    description: str
    completed: bool = False

    class Config:
        orm_mode = True