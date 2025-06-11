from fastapi import APIRouter, Depends, status, HTTPException, Query
from fastapi.responses import Response
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from services import MemberService, MemberMissionService
from sqlalchemy.orm import Session
from db.session import get_session
from datetime import date
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def get_member_mission_service(db: Session = Depends(get_session)) -> MemberMissionService:
    return MemberMissionService(db)

# 🚩회원 미션 관련 API

@router.get("/members/{member_seq}/missions/latest", 
            summary="사용자의 가장 최근 미션 조회")
def get_latest_mission_by_member(
    member_seq: int,
    member_mission_service: MemberMissionService = Depends(get_member_mission_service)
):
    latest_mission = member_mission_service.get_latest_mission(member_seq)
    if not latest_mission:
        raise HTTPException(status_code=404, detail="최근 생성된 미션이 없습니다.")
    return latest_mission

@router.get("/members/{member_seq}/missions", 
            summary="사용자의 전체 미션 목록 조회 (최신순)")
def get_all_missions_by_member(
    member_seq: int,
    member_mission_service: MemberMissionService = Depends(get_member_mission_service)
):
    missions = member_mission_service.get_all_mission(member_seq)
    if not missions:
        raise HTTPException(status_code=404, detail="미션 기록이 없습니다.")
    return missions

@router.get("/members/{member_seq}/missions/date", summary="사용자의 특정 날짜 미션 조회")
def get_mission_by_member_and_date(
    member_seq: int,
    target_date: date = Query(..., description="조회할 날짜 (YYYY-MM-DD)"),
    member_mission_service: MemberMissionService = Depends(get_member_mission_service)
):
    mission = member_mission_service.get_mission_by_date(member_seq, target_date)
    if not mission:
        raise HTTPException(status_code=404, detail="해당 날짜의 미션이 없습니다.")
    return mission

@router.patch("/members/missions/{member_mission_seq}/complete", summary="미션 완료 처리")
def complete_mission_by_id(
    member_mission_seq: int,
    member_mission_service: MemberMissionService = Depends(get_member_mission_service)
):
    updated = member_mission_service.complete_mission(member_mission_seq)
    if not updated:
        raise HTTPException(status_code=404, detail="미션 완료 처리에 실패했습니다.")
    return {"message": "미션이 완료되었습니다."}

@router.delete("/members/missions/{member_mission_seq}", 
               status_code=HTTP_204_NO_CONTENT)
def delete_member_mission(member_mission_seq: int, 
                          member_mission_service: MemberMissionService = Depends(get_member_mission_service)):
    success = member_mission_service.delete_member_mission(member_mission_seq)

    if not success:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="MemberMission not found")
    