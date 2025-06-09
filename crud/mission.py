from sqlalchemy.orm import Session
from models.mission import Mission
from typing import Optional


def create_mission(db: Session, content: str, emotion_seq: int):
    """
    미션을 생성합니다.
    """
    mission = Mission(
        content=content,
        emotion_seq=emotion_seq
    )
    db.add(mission)
    db.commit()

def update_mission(db: Session, mission_seq: int, content: Optional[str] = None, emotion_seq: Optional[int] = None) -> Mission | None:
    mission = db.get(Mission, mission_seq)
    if not mission:
        return None
    if content is not None:
        mission.content = content
    if emotion_seq is not None:
        mission.emotion_seq = emotion_seq
    db.add(mission)
    db.commit()
    db.refresh(mission)
    return mission

        
