from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_session
from services import MissionService, MemberMissionService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def get_mission_service(db: Session = Depends(get_session)) -> MissionService:
    return MissionService(db)

def get_member_mission_service(db: Session = Depends(get_session)) -> MemberMissionService:
    return MemberMissionService(db)

@router.get("/{mission_seq}", summary="미션 ID로 단일 미션 조회")
async def get_mission(
    mission_seq: int,
    mission_service: MissionService = Depends(get_mission_service)
):
    mission = await mission_service.get_mission(mission_seq)
    if not mission:
        raise HTTPException(status_code=404, detail="해당 미션을 찾을 수 없습니다.")
    return mission