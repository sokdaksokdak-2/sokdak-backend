# db/init_db.py

from sqlmodel import SQLModel
from db.session import engine
from models import Member, Emotion, Mission, MemberMission, EmotionCalendarEntry

# models에서 정의된 모든 테이블을 가져와서 DB에 생성
def init_db():
    SQLModel.metadata.create_all(engine)
