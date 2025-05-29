from sqlmodel import SQLModel
from .session import engine

# models에서 정의된 모든 테이블을 가져와서 DB에 생성
def init_db():
    SQLModel.metadata.create_all(engine)


