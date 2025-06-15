from sqlalchemy.orm import Session
from crud import mission as mission_crud
from schemas import CreateMissionRequestDto


class MissionService:
    def __init__(self, db: Session):
        self.db = db
        self.mission_crud = mission_crud
    

    async def get_all_missions(self) -> list:
        """
        모든 미션 조회
        """
        missions = self.mission_crud.get_missions(self.db)        
        return missions

    async def create_mission(self, request: CreateMissionRequestDto) : 
        """
        미션을 생성합니다.
        """
        self.mission_crud.create_mission(
            db=self.db,
            content = request.content,
            emotion_detail_seq = request.emotion_detail_seq
        )
    
    async def get_mission(self, mission_seq: int):
        return self.mission_crud.get_mission_by_mission_seq(self.db, mission_seq=mission_seq)