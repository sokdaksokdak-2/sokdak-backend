from pydantic import BaseModel

class MemberMissionResponseDto(BaseModel) :
    member_mission_seq: int
    completed: int
    content: str
    emotion_seq: int
    emotion_score: int
    title: str
    
class MissionSuggestionDto(BaseModel) :
    emotion_seq: int
    emotion_score: int
    mission_seq: int
    title: str

class MemberMissionSimpleDto(BaseModel) :
    member_mission_seq : int
    content : str
    title : str
    completed : int
    emotion_seq: int
    emotion_score: int