from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_session
from services.mission_service import MissionService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def get_mission_service(db: Session = Depends(get_session)) -> MissionService:
    return MissionService(db)

@router.get("/missions/{member_seq}",
            summary="미션 목록 조회")
async def get_messions(
    member_seq: int,
    mission_service: MissionService = Depends(get_mission_service)
) -> list:
    if not member_seq:
        raise HTTPException(status_code=400, detail="member_seq가 없습니다.")
    
    return await mission_service.get_missions(member_seq)


@router.post("/missions/create",
            summary="미션 생성")