from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.db.database import Base

# класс Story создаёт ORM-модель (таблицу в БД), унаследованную от Base
# Base - объект, созданный через declarative_base() - он говорит SQLAlchemy, что это таблица
#  __tablename__ = "stories" - указывает имя таблицы в БД (БД - stories)
class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    session_id = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    nodes= relationship("StoryNode", back_populates="story")

class StoryNode(Base):
    __tablename__ = "story_nodes"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id"), index=True)
    content = Column(String)
    is_root = Column(Boolean, default=False)
    is_ending = Column(Boolean, default=False)
    is_winning = Column(Boolean, default=False)
    options = Column(JSON, default=list)

    story = relationship("Story", back_populates="nodes")
