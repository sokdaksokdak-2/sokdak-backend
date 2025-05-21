from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from models.member import Member
from models.mission import Mission

class MemberMission(SQLModel, table=True):
    __tablename__ = "member_mission"

    member_mission_seq: Optional[int] = Field(default=None, primary_key=True)
    date_assigned: date
    completed: Optional[bool] = False
    date_completed: Optional[date] = None

    member_seq2: int = Field(foreign_key="member.member_seq")
    mission_seq2: int = Field(foreign_key="mission.mission_seq")

    member: Optional[Member] = Relationship()
    mission: Optional[Mission] = Relationship()
