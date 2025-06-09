from sqlalchemy.orm import Session
from sqlalchemy import select
from models.mission import Mission
from models.member_mission import MemberMission
from models.emotion_detail import EmotionDetail
import random

def get_member_missions_by_member_seq(db: Session, member_seq: int) -> list[MemberMission]:
    """
    주어진 member_seq에 대한 미션 목록을 조회합니다.
    """
    return (
        db.query(MemberMission)
        .filter(MemberMission.member_seq == member_seq)
        .order_by(MemberMission.date_assigned)
        .all()
    )

def get_member_mission_by_member_mission_seq(
    db: Session, member_mission_seq: int
) -> MemberMission | None :
    """
    주어진 member_mission_seq에 대한 미션을 조회합니다.
    """
    return (
        db.query(MemberMission)
        .filter(MemberMission.member_mission_seq == member_mission_seq)
        .first()
    )


def get_latest_member_mission_by_member_seq(db: Session, member_seq: int) -> MemberMission | None :
    """
    주어진 member_seq에 대한 가장 최근 미션 조회
    """
    return (
        db.query(MemberMission)
        .filter(MemberMission.member_seq == member_seq)
        .order_by(MemberMission.date_assigned.desc())
        .first()
    )


def create_member_mission(
    db: Session, member_seq: int, emotion_seq: int, emotion_score: int
) :
    """
    주어진 member_seq와 감정+강도(emotion_seq, emotion_score)에 맞는 미션을 생성
    """
    # 1. emotion_detail 조회
    emotion_detail =(
        db.query(EmotionDetail)
        .filter(EmotionDetail.emotion_seq == emotion_seq, 
                EmotionDetail.emotion_score == emotion_score)
        .first()
    )
    
    if not emotion_detail:
        raise ValueError("해당 감정과 강도에 맞는 감정 상세 정보가 없습니다.")
    
    # 2. 사용자가 최근에 수행한 미션 조회
    recent_assigned_missions_subq = (
        db.query(MemberMission)
        .filter(MemberMission.member_seq == member_seq)
        .order_by(MemberMission.date_assigned.desc())
        .limit(7) # 최근 7개 미션 조회
        .subquery()
    )

    # 3. 최근 수행한 미션과 중복되지 않은 미션 필터링
    available_missions = (
        db.query(Mission)
        .filter(Mission.emotion_detail_seq == emotion_detail.emotion_detail_seq)
        .filter(Mission.mission_seq.not_in(select(recent_assigned_missions_subq.c.mission_seq)))
        .all()
    )

    if not available_missions: # 전부 최근에 수행한 미션이라면
        available_missions = (
            db.query(Mission)
            .filter(Mission.emotion_detail_seq == emotion_detail.emotion_detail_seq)
            .all()
        )

    # 4. 랜덤으로 하나 선택
    selected_mission = random.choice(available_missions)


    # 5. MemberMission 생성
    member_mission = MemberMission(
        member_seq=member_seq,
        mission_seq=selected_mission.mission_seq,
    )
    db.add(member_mission)
    db.commit()
    db.refresh(member_mission)
    return member_mission

