from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_session
from services.member_mission_service import MemberMissionService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def get_member_mission_service(db: Session = Depends(get_session)) -> MemberMissionService:
    return MemberMissionService(db)

@router.get("/latest/{member_seq}")
def get_latest_mission(member_seq: int, db: Session = Depends(get_db)):
    service = MemberMissionService(db)
    result = service.get_latest_member_mission_by_member_seq(member_seq)
    if not result:
        raise HTTPException(status_code=404, detail="최근 미션이 없습니다.")
    return result