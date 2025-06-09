from sqlalchemy.orm import Session
from models.mission import Mission
from typing import Optional


def create_mission(db: Session, content: str, emotion_seq: int):
    """
    미션을 생성합니다.
    """
    mission = Mission(
        content=content,
        emotion_detail_seq=emotion_seq
    )
    db.add(mission)
    db.commit()

# TODO : 라우터 아직 없음
def update_mission(db: Session, mission_seq: int, content: Optional[str] = None, emotion_detail_seq: Optional[int] = None) -> Mission | None:
    mission = db.get(Mission, mission_seq)
    if not mission:
        return None
    if content is not None:
        mission.content = content
    if emotion_detail_seq is not None:
        mission.emotion_detail_seq = emotion_detail_seq
    db.add(mission)
    db.commit()
    db.refresh(mission)
    return mission

def get_missions(db: Session) -> list[Mission]:
    """
    모든 미션을 조회합니다.
    """
    return db.query(Mission).all()
        
def get_mission_by_mission_seq(db: Session, mission_seq: int) -> Mission | None:
    """
    주어진 mission_seq에 해당하는 미션을 조회합니다.
    """
    return db.query(Mission).filter(Mission.mission_seq == mission_seq).first()