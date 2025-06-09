from sqlalchemy.orm import Session
from models.mission import Mission
from models.member_mission import MemberMission


def get_member_missions_by_member_seq(db: Session, member_seq: int) -> list[MemberMission]:
    """
    주어진 member_seq에 대한 미션 목록을 조회합니다.
    """
    return db.query(MemberMission).filter(MemberMission.member_seq == member_seq).order_by(MemberMission.date_assigned).all()

def get_member_mission_by_member_mission_seq(
    db: Session, member_mission_seq: int
) -> MemberMission | None :
    """
    주어진 member_mission_seq에 대한 미션을 조회합니다.
    """
    return db.query(MemberMission).filter(MemberMission.member_mission_seq == member_mission_seq).first()

def create_static_member_mission_(
    db: Session, member_seq: int, mission_seq: int
) :
    """
    주어진 member_seq와 mission_seq에 대한 미션을 생성합니다.
    """
    member_mission = MemberMission(
        member_seq=member_seq,
        mission_seq=mission_seq
    )
    db.add(member_mission)
    db.commit()
    

def create_gpt_member_mission(
    db: Session, member_seq: int, mission_text: str
) :
    """
    GPT 미션을 생성합니다.
    """

    member_mission = MemberMission(
        member_seq=member_seq,
        custom_mission_text=mission_text
    )
    db.add(member_mission)
    db.commit()
    
    return member_mission