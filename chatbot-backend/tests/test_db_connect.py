
from sqlalchemy import inspect  # SQLAlchemy의 inspect 모듈을 사용하여 DB 테이블 확인
from sqlalchemy import text # SQLAlchemy의 text 모듈을 사용하여 SQL 쿼리 실행
from sqlmodel import SQLModel, create_engine, select
from models import Member, Emotion, Mission, MemberMission, EmotionCalendar, EmotionCalendarDetail, MemberOAuth
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session

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



# 감정 이름과 캐릭터 이미지 경로 예시
emotion_data = [
    ("기쁨", "joy", "#FDC420", "joy"),
    ("슬픔", "sadness", "#4a7edf", "sad"),
    ("불안", "anxiety", "#FC5F15", "anxious"),
    ("화남", "anger", "#be2d35", "angry"),
    ("중립", "neutral", "#8ED465", "neutral"),
]

# 감정 강도별 데이터 생성 (1: 낮음, 2: 보통, 3: 강함)
def generate_emotion_variants():
    emotions = []
    for name_k, name_e, color, image_name in emotion_data:
        for score in range(1, 4):  # 1~3
            emotions.append(
                Emotion(
                    name_kr=f"{name_k}_{score}",
                    name_en=f"{name_e}_{score}",
                    color_code=color,
                    character_image_url=f"assets/characters/{image_name}_{score}.png",  # Flutter 기준 asset 경로
                    emotion_score=score
                )
            )
    return emotions

def test_insert_emotion_data():
    engine = create_engine(DATABASE_URL, echo=True)
    print("▶️ 감정 데이터 삽입 및 검증 시작...")

    SQLModel.metadata.create_all(engine)
    emotions = generate_emotion_variants()

    with Session(engine) as session:
        # 🔥 기존 데이터 삭제
        session.execute(text("DELETE FROM emotion"))
        session.commit()

        # 🔥 새 데이터 삽입
        session.add_all(emotions)
        session.commit()
        print("✅ 감정 데이터 삽입 완료!")

        # 🔍 검증용 쿼리
        results = session.execute(select(Emotion)).scalars().all()
        assert len(results) == 15, f"❌ 예상한 15개 감정 중 {len(results)}개만 들어감"
        print("✅ 감정 데이터 개수 검증 통과 (15개)")

        joy_3 = next((e for e in results if e.name_kr == "기쁨_3"), None)
        assert joy_3 is not None, "❌ '기쁨_3' 감정 없음"
        assert joy_3.emotion_score == 3, "❌ '기쁨_3' emotion_score 잘못됨"
        print("✅ '기쁨_3' 데이터 검증 통과")

    print("🎉 전체 감정 데이터 삽입 및 검증 테스트 완료!")