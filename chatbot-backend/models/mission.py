from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from models.emotion import Emotion

class Mission(SQLModel, table=True):
    __tablename__ = "mission"
    
    mission_seq: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    emotion_seq: int = Field(foreign_key="emotion.emotion_seq")
    emotion: Optional[Emotion] = Relationship()
