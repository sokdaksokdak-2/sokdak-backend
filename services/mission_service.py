from sqlalchemy.orm import Session
from models.mission import Mission
from crud.mission import mission_crud




class MissionService:
    def __init__(self, db: Session):
        self.db = db
        self.mission_crud = mission_crud
    

    async def get_missions(self, member_seq: int) -> list:
        """
        주어진 member_seq에 대한 미션 목록을 조회합니다.
        """

        missions = self.mission_crud.get_missions_by_member_seq(self.db, member_seq)
        
        return missions

    async def create_mission_(self, content: str, emotion_seq: int) : 
        """
        미션을 생성합니다.
        """
        mission = Mission(
            content=content,
            emotion_seq=emotion_seq
        )