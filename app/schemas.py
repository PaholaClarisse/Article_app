from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ArticleCreate(BaseModel):
    title : str
    content: str
    author: str
    category: Optional[str] = None
    tags: Optional[str] = None

class ArticleUpdate(BaseModel):
    title : Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None

class ArticleOut(BaseModel):
    id: int
    title : str
    content: str
    author: str
    created_at: datetime
    category: Optional[str] = None
    tags: Optional[str] = None

    class config:
        orm_model = True

