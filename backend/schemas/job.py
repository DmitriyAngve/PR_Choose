from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class StoryJobBase(BaseModel):
    theme: str


# class Config: from_attributes = True - это настройка внутри Config, которая говорит Pydantic:
# разреши мне создавать эту модель не только из dict, но и из обычных Python-моделей (например, SQLAlchemy)

class StoryJobResponse(BaseModel):
    job_id: int
    status: str
    created_at: datetime
    story_id: Optional[int] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None

    class Config:
        from_attributes = True


class StoryJobCreate(StoryJobBase):
    pass