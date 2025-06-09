from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_session
from services.mission_service import MissionService
from schemas.mission import CreateMissionRequestDto
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def get_mission_service(db: Session = Depends(get_session)) -> MissionService:
    return MissionService(db)

# TODO : 미완성, 미션내용, 감정번호?, 감정강도?, 미션 배정일, 미션 완료일, 미션완료
# GET /missions/item/{mission_seq}
@router.get("/item/{mission_seq}")
def get_mission_by_seq(mission_seq: int, member_mission_service: MissionService = Depends(get_mission_service)):
    mission = member_mission_service.get_mission_by_mission_seq(mission_seq)
    if not mission:
        raise HTTPException(status_code=404, detail="해당 미션을 찾을 수 없습니다.")
    return mission

# @router.get("/list",
#             summary="미션 목록 조회 - 추후 관리자")
# async def get_messions(
#     mission_service: MissionService = Depends(get_mission_service)
# ) -> list:
#     return await mission_service.get_missions()


# @router.post("/create",
#             summary="미션 생성")
# async def create_mission(
#     request: CreateMissionRequestDto,
#     mission_service: MissionService = Depends(get_mission_service)
# ):
#     mission_service.create_mission(request)