from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from crud import member_mission as member_mission_crud
from schemas.mission import MemberMissionSeqDto
from schemas.member_mission import MemberMissionResponseDto
from datetime import date
import logging
import random

logger = logging.getLogger(__name__)

class MemberMissionService:
    def __init__(self, db: Session):
        self.db = db

    def create_member_mission(self, member_seq: int, emotion_seq: int, emotion_score: int):
        """
        미션 생성 - 랜덤 미션 선택 로직 포함
        """
        try:
            with self.db.begin():
                # 1. 감정 상세 정보 조회
                emotion_detail = member_mission_crud.get_emotion_detail(
                    self.db, emotion_seq, emotion_score
                )
                if not emotion_detail:
                    raise ValueError("해당 감정과 강도에 맞는 감정 상세 정보가 없습니다.")

                # 2. 최근 수행한 미션 ID 목록 조회
                recent_mission_ids = member_mission_crud.get_recent_mission_ids(self.db, member_seq)

                # 3. 사용 가능한 미션 목록 조회
                available_missions = member_mission_crud.get_available_missions(
                    self.db, emotion_detail.emotion_detail_seq, recent_mission_ids
                )

                # 4. 사용 가능한 미션이 없으면 최근 미션 제외 조건을 해제하고 재조회
                if not available_missions:
                    available_missions = member_mission_crud.get_available_missions(
                        self.db, emotion_detail.emotion_detail_seq, []
                    )

                if not available_missions:
                    logger.error("해당 감정 상세에 매핑된 미션이 없습니다.")
                    raise ValueError("사용 가능한 미션이 없습니다.")

                # 5. 랜덤 미션 선택
                selected_mission = random.choice(available_missions)

                # 6. 미션 레코드 생성
                member_mission = member_mission_crud.create_member_mission_record(
                    self.db, member_seq, selected_mission.mission_seq
                )

                return MemberMissionSeqDto(
                    member_mission_seq=member_mission.member_mission_seq
                )
        except SQLAlchemyError as e:
            logger.error(f"미션 생성 중 데이터베이스 오류 발생: {str(e)}")
            raise Exception("미션 생성에 실패했습니다.")
        except Exception as e:
            logger.error(f"미션 생성 중 예외 발생: {str(e)}")
            raise Exception("미션 생성 중 오류가 발생했습니다.")
    
    def get_latest_mission(self, member_seq: int):
        """
        사용자의 가장 최근 배정된 미션
        """
        try:
            result = member_mission_crud.get_latest_member_mission_by_member_seq(self.db, member_seq)
            if not result:
                return None
            member_mission, mission, emotion_detail = result
            return MemberMissionResponseDto(
                member_mission_seq=member_mission.member_mission_seq,
                mission_seq=mission.mission_seq,
                content=mission.content,
                emotion_seq=emotion_detail.emotion_seq,
                emotion_score=emotion_detail.emotion_score,
            )
        except SQLAlchemyError as e:
            logger.error(f"최근 미션 조회 중 데이터베이스 오류 발생: {str(e)}")
            raise Exception("미션 조회에 실패했습니다.")
        except Exception as e:
            logger.error(f"최근 미션 조회 중 예외 발생: {str(e)}")
            raise Exception("미션 조회 중 오류가 발생했습니다.")

    def get_all_mission(self, member_seq: int):
        """
        사용자의 전체 미션 목록 조회 - 날짜 내림차순
        """
        try:
            return member_mission_crud.get_member_missions_by_member_seq(self.db, member_seq)
        except SQLAlchemyError as e:
            logger.error(f"전체 미션 조회 중 데이터베이스 오류 발생: {str(e)}")
            raise Exception("미션 목록 조회에 실패했습니다.")
        except Exception as e:
            logger.error(f"전체 미션 조회 중 예외 발생: {str(e)}")
            raise Exception("미션 목록 조회 중 오류가 발생했습니다.")

    def get_mission_by_date(self, member_seq: int, target_date: date):
        """
        사용자와 날짜로 특정 미션 조회
        """
        try:
            return member_mission_crud.get_member_mission_by_member_seq_and_date(
                self.db, member_seq, target_date
            )
        except SQLAlchemyError as e:
            logger.error(f"날짜별 미션 조회 중 데이터베이스 오류 발생: {str(e)}")
            raise Exception("미션 조회에 실패했습니다.")
        except Exception as e:
            logger.error(f"날짜별 미션 조회 중 예외 발생: {str(e)}")
            raise Exception("미션 조회 중 오류가 발생했습니다.")

    def get_mission_by_member_mission_seq(self, member_mission_seq: int):
        """
        미션 ID로 단일 미션 조회
        """
        try:
            return member_mission_crud.get_mission_by_member_mission_seq(self.db, member_mission_seq)
        except SQLAlchemyError as e:
            logger.error(f"미션 조회 중 데이터베이스 오류 발생: {str(e)}")
            raise Exception("미션 조회에 실패했습니다.")
        except Exception as e:
            logger.error(f"미션 조회 중 예외 발생: {str(e)}")
            raise Exception("미션 조회 중 오류가 발생했습니다.")

    def complete_mission(self, member_mission_seq: int):
        """
        미션 완료 처리
        """
        try:
            updated = member_mission_crud.update_mission_status_to_completed(
                self.db, member_mission_seq
            )
            if not updated:
                raise Exception("해당 미션을 찾을 수 없습니다.")
            return updated
        except SQLAlchemyError as e:
            logger.error(f"미션 완료 처리 중 데이터베이스 오류 발생: {str(e)}", exc_info=True)
            raise Exception("미션 완료 처리에 실패했습니다.")
        except Exception as e:
            logger.error(f"미션 완료 처리 중 예외 발생: {str(e)}", exc_info=True)
            raise Exception("미션 완료 처리 중 오류가 발생했습니다.")

    def delete_member_mission(self, member_mission_seq: int):
        """미션 포기 - 삭제"""
        try:
            with self.db.begin():
                return member_mission_crud.delete_member_mission(self.db, member_mission_seq)
        except SQLAlchemyError as e:
            logger.error(f"미션 삭제 중 데이터베이스 오류 발생: {str(e)}")
            raise Exception("미션 삭제에 실패했습니다.")
        except Exception as e:
            logger.error(f"미션 삭제 중 예외 발생: {str(e)}")
            raise Exception("미션 삭제 중 오류가 발생했습니다.")