# db/session.py - DB 연결과 세션 생성

from sqlmodel import create_engine, Session
from core.config import settings

engine = create_engine(settings.database_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
