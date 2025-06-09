from sqlalchemy.orm import Session
from crud import member_mission as member_mission_crud
from schemas.mission import MissionSeqDto


class MemberMissionService:
    def __init__(self, db: Session):
        self.db = db

    def create_member_mission(self, member_seq: int, emotion_seq: int, emotion_score: int):
        """
        회원의 미션을 생성합니다.
        :param member_seq: 회원의 고유 식별자
        :param emotion_seq: 감정 시퀀스
        :param emotion_score: 감정 강도 점수
        :return: 생성된 미션 seq
        """
        member_mission = member_mission_crud.create_member_mission(self.db, member_seq, emotion_seq, emotion_score)
        return MissionSeqDto(member_mission.mission_seq)


    def get_latest_member_mission_by_member_seq(self, member_seq: int):
        """
        회원의 가장 최근미션 정보 조회
        :param member_seq
        :return : 회원의 가장 최근 미션 정보
        """
        return member_mission_crud.get_latest_member_mission_by_member_seq(self.db, member_seq)
    
    def get_member_missions_by_member_seq(self, member_seq: int) :
        """
        회원의 미션 목록 조회
        :param member_seq: 회원의 고유 식별자
        :return: 회원의 미션 목록
        """
        return member_mission_crud.get_member_missions_by_member_seq(self.db, member_seq)
    
    def get_member_mission_by_member_mission_seq(self, member_mission_seq: int):
        """
        회원의 특정 미션 정보 조회
        :param member_mission_seq: 회원 미션의 고유 식별자
        :return: 회원의 특정 미션 정보
        """
        return member_mission_crud.get_member_mission_by_member_mission_seq(self.db, member_mission_seq)