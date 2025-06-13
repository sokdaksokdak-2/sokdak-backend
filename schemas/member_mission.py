from pydantic import BaseModel

class MemberMissionResponseDto(BaseModel) :
    member_mission_seq: int
    completed: int
    content: str
    emotion_seq: int
    emotion_score: int
    title: str
    
class EmotionSeqScoreAndCalendarDetailTitleDto(BaseModel) :
    emotion_seq: int
    emotion_score: int
    title: str

class MemberMissionSimpleDto(BaseModel) :
    member_mission_seq : int
    content : str
    title : str
    completed : int