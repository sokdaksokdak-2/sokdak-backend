from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, UTC

class MemberMission(SQLModel, table=True):
    """회원과 미션의 다대다 관계를 나타내는 조인 테이블"""
    __tablename__ = "member_mission"

    # member, mission 조인 테이블

    member_mission_seq: Optional[int] = Field(default=None, primary_key=True)
    date_assigned: datetime = Field(default_factory=lambda: datetime.now(UTC)) # 배정일, 시간 포함
    completed: Optional[bool] = Field(default=False)
    date_completed: Optional[datetime] = Field(default=None) # 완료된 경우만 값 있음
    custom_mission_text: Optional[str] = Field(default=None, description="gpt로 생성된 미션")

    # 다대다 관계 테이블 이므로 member_seq, mission_seq 반드시 필요
    mission_seq: int = Field(nullable=False)
    member_seq: int = Field(nullable=True) # DB에 저장된 미션, GPT를 이용해 생성한 미션 2가지 경우 존재

