from pydantic import BaseModel

class MemberMissionResponseDto(BaseModel) :
    member_mission_seq: int
    mission_seq: int
    content: str
    emotion_seq: int
    emotion_score: int