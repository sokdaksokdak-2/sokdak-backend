# db 연결 및 테이블 생성 확인 -> ROOT 폴더 파일 이동시켜서 테스트(안그럼 루트꼬임~)

from sqlalchemy import inspect  # SQLAlchemy의 inspect 모듈을 사용하여 DB 테이블 확인
from sqlalchemy import text # SQLAlchemy의 text 모듈을 사용하여 SQL 쿼리 실행
from sqlmodel import SQLModel, create_engine
from models import Member, Emotion, Mission, MemberMission, EmotionCalendar, EmotionCalendarDetail, MemberOAuth
from dotenv import load_dotenv
import os
# MySQL 연결 문자열
# 형식: mysql+pymysql://<유저이름>:<비밀번호>@<호스트>/<DB이름>
# DATABASE_URL = "mysql+pymysql://root:123456@localhost/whisper_db"
DATABASE_URL="mysql+pymysql://campus_LGDX6_p3_1:smhrd1@project-db-campus.smhrd.com:3307/campus_LGDX6_p3_1"
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def test_db_connection():
    print("▶️MySQL 연결 테스트 시작...")
    # SQLModel을 사용하여 MySQL 데이터베이스 연결
    # SQLModel은 SQLAlchemy를 기반으로 하므로, SQLAlchemy의 create_engine을 사용하여 연결
    # SQLModel은 SQLAlchemy의 ORM을 사용하여 데이터베이스와 상호작용함
    try:
        engine = create_engine(DATABASE_URL, echo=True)  # echo=True 하면 쿼리 로그도 보여줌)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")) # 1이라는 간단한 쿼리를 실행하여 DB 연결 확인
            assert result.scalar() == 1
        print("✅ DB 연결 성공!")
    except Exception as e:
        print("❌ DB 연결 실패:", e)
        assert False

def test_drop_tables():
    print("▶️모든 테이블 삭제 시작...")
    engine = create_engine(DATABASE_URL)
    SQLModel.metadata.drop_all(engine)
    print("✅모든 테이블 삭제 완료!")

def test_table_creation():
    print("▶️MySQL 테이블 생성 테스트 시작...")
    engine = create_engine(DATABASE_URL)
    # 모델 import 후 테이블 생성 시도
    SQLModel.metadata.create_all(engine)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("생성된 테이블:", tables)  # 디버깅을 위해 실제 생성된 테이블 출력
    
    expected_tables = [
        "member", 
        "emotion", 
        "mission", 
        "member_mission", 
        "emotion_calendar",
        "emotion_calendar_details",
        "member_oauth",
        "emotion_report"
    ]
    for table in expected_tables:
        assert table in tables, f"'{table}' 테이블이 생성되지 않았습니다."
    print("✅테이블 생성 완료!")


    
