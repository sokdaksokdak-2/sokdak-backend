from pydantic import BaseModel

class CreateMissionRequestDto(BaseModel):
    content:str
    emotion_detail_seq:int

class MissionDto(BaseModel):
    mission_seq: int
    content: str
    emotion_detail_seq: int

class MissionSeqDto(BaseModel) :
    mission_seq: int