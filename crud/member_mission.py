from sqlalchemy.orm import Session
from sqlalchemy import cast, Date
from models import Mission, MemberMission, EmotionDetail
from datetime import date, datetime, UTC
import logging

logger = logging.getLogger(__name__)

def get_member_missions_by_member_seq(db: Session, member_seq: int) -> list[MemberMission]:
    """특정 회원의 모든 미션을 날짜순으로 조회"""
    return (
        db.query(MemberMission)
        .filter(MemberMission.member_seq == member_seq)
        .order_by(MemberMission.date_assigned.desc())
        .all()
    )

def get_mission_by_member_mission_seq(db: Session, mission_seq: int) -> tuple[MemberMission, Mission, EmotionDetail] | None:
    """맴버미션 ID로 단일 미션 조회"""
    return (
        db.query(MemberMission, Mission, EmotionDetail)
        .join(Mission, MemberMission.mission_seq == Mission.mission_seq)
        .join(EmotionDetail, Mission.emotion_detail_seq == EmotionDetail.emotion_detail_seq)
        .filter(MemberMission.mission_seq == mission_seq)
        .first()
    )

def get_latest_member_mission_by_member_seq(db: Session, member_seq: int) -> tuple[MemberMission, Mission, EmotionDetail] | None:
    """특정 회원의 가장 최신 미션 조회"""
    return (
        db.query(MemberMission, Mission, EmotionDetail)
        .join(Mission, MemberMission.mission_seq == Mission.mission_seq)
        .join(EmotionDetail, Mission.emotion_detail_seq == EmotionDetail.emotion_detail_seq)
        .filter(MemberMission.member_seq == member_seq)
        .order_by(MemberMission.date_assigned.desc())
        .first()
    )

def get_emotion_detail(db: Session, emotion_seq: int, emotion_score: int) -> EmotionDetail | None:
    """감정 시퀀스와 점수로 감정 상세 조회"""
    return (
        db.query(EmotionDetail)
        .filter(
            EmotionDetail.emotion_seq == emotion_seq,
            EmotionDetail.emotion_score == emotion_score
        )
        .first()
    )

def get_recent_mission_ids(db: Session, member_seq: int, limit: int = 7) -> list[int]:
    """최근 수행한 미션 ID 목록 조회"""
    recent_missions_subq = (
        db.query(MemberMission.mission_seq)
        .filter(MemberMission.member_seq == member_seq)
        .order_by(MemberMission.date_assigned.desc())
        .limit(limit)
        .subquery()
    )
    return [row[0] for row in db.query(recent_missions_subq).all()]

def get_available_missions(db: Session, emotion_detail_seq: int, excluded_mission_ids: list[int]) -> list[Mission]:
    """감정 상세에 해당하며 제외된 미션을 뺀 미션 목록 조회"""
    query = db.query(Mission).filter(Mission.emotion_detail_seq == emotion_detail_seq)
    if excluded_mission_ids:
        query = query.filter(~Mission.mission_seq.in_(excluded_mission_ids))
    return query.all()

def create_member_mission_record(db: Session, member_seq: int, mission_seq: int) -> MemberMission:
    """새로운 회원 미션 레코드 생성"""
    new_member_mission = MemberMission(
        member_seq=member_seq,
        mission_seq=mission_seq,
    )
    db.add(new_member_mission)
    db.commit()
    db.refresh(new_member_mission)
    return new_member_mission

def get_member_mission_by_member_seq_and_date(db: Session, member_seq: int, target_date: date) -> MemberMission | None:
    """사용자와 날짜로 미션 해당 날짜 조회"""
    return db.query(MemberMission).filter(
        MemberMission.member_seq == member_seq,
        cast(MemberMission.date_assigned, Date) == target_date
    ).all()

def update_mission_status_to_completed(db: Session, member_mission_seq: int) -> MemberMission | None:
    """미션 완료상태로 변경"""
    mission = db.query(MemberMission).filter(
        MemberMission.member_mission_seq == member_mission_seq
    ).first()

    if mission:
        mission.completed = True
        mission.date_completed = datetime.now(UTC)
        db.commit()
        db.refresh(mission)
    
    return mission

def delete_member_mission(db: Session, member_mission_seq: int) -> bool:
    """미션 삭제"""
    mission = db.query(MemberMission).filter(
        MemberMission.member_mission_seq == member_mission_seq
    ).first()

    if mission:
        db.delete(mission)
        db.commit()
        return True
    return False