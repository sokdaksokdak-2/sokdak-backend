from sqlalchemy.orm import Session, aliased
from models.emotion_report import EmotionReport
from models import EmotionCalendarDetail, EmotionCalendar, Emotion
from datetime import date

def get_emotion_report(db: Session, member_seq: int, report_date: date):
    """
    특정 회원의 특정 월(1일 기준) 감정 리포트를 조회합니다.
    """
    month_start = report_date.replace(day=1)
    return db.query(EmotionReport).filter(
        EmotionReport.member_seq == member_seq,
        EmotionReport.report_date == month_start
    ).first()

def save_emotion_report(db: Session, report: EmotionReport):
    """
    감정 리포트 객체를 DB에 저장하고, 갱신된 객체를 반환합니다.
    """
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

def get_monthly_emotion_stats(db: Session, member_seq: int, start_date: date, end_date: date):
    """
    전달 월의 감정별 (emotion_seq, 강도, count) raw 데이터를 반환합니다.
    
    Parameters:
    - db: SQLAlchemy 세션 객체
    - member_seq: 회원 식별 번호
    - start_date: 조회 시작일
    - end_date: 조회 종료일

    Returns:
    - [(emotion_seq, emotion_score, count), ...] 형태의 리스트 반환
    """

    from sqlalchemy import func  # 집계 함수를 사용하기 위해 func를 import

    try:
        EmotionAlias = aliased(Emotion)
        EmotionDetailAlias = aliased(EmotionCalendarDetail)

        result = (
            db.query(
                EmotionAlias.emotion_seq,
                EmotionDetailAlias.emotion_score,
                func.count().label("count")
            )
            .join(EmotionCalendarDetail, EmotionCalendarDetail.emotion_seq == EmotionAlias.emotion_seq)
            .join(EmotionCalendar, EmotionCalendarDetail.calendar_seq == EmotionCalendar.calendar_seq)
            .join(EmotionDetailAlias, Emotion.emotion_seq == EmotionDetailAlias.emotion_seq) 
            .filter(
                EmotionCalendar.member_seq == member_seq,
                EmotionCalendar.calendar_date >= start_date,
                EmotionCalendar.calendar_date <= end_date
            )
            .group_by(EmotionAlias.emotion_seq, EmotionDetailAlias.emotion_score)
            .all()
        )
        return result or []  # ← 쿼리 결과가 없으면 빈 리스트 반환
    except Exception as e:
        print(f"[ERROR] Failed to fetch emotion stats: {e}")
        return []


def get_monthly_contexts(db: Session, member_seq: int, start_date: date, end_date: date):
    """
    전달 월의 감정 메모 context 리스트를 반환합니다.
    - 반환: [context, ...]
    """
    contexts = db.query(EmotionCalendarDetail.context
    ).join(EmotionCalendar, EmotionCalendar.calendar_seq == EmotionCalendarDetail.calendar_seq
    ).filter(
        EmotionCalendar.member_seq == member_seq,
        EmotionCalendar.calendar_date >= start_date,
        EmotionCalendar.calendar_date <= end_date,
        EmotionCalendarDetail.context.isnot(None)
    ).all()
    return [c[0] for c in contexts if c[0]]

