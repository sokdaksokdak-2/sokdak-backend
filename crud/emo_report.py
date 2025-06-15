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
    from sqlalchemy import func

    try:
        result = (
            db.query(
                EmotionCalendarDetail.emotion_seq.label("emotion_seq"),
                func.sum(EmotionCalendarDetail.emotion_score).label("score_sum"),
                func.count(EmotionCalendarDetail.detail_seq).label("count")
            )
            .join(EmotionCalendar, EmotionCalendarDetail.calendar_seq == EmotionCalendar.calendar_seq)
            .filter(
                EmotionCalendar.member_seq == member_seq,
                EmotionCalendar.calendar_date >= start_date,
                EmotionCalendar.calendar_date <= end_date
            )
            .group_by(EmotionCalendarDetail.emotion_seq)
            .order_by(func.sum(EmotionCalendarDetail.emotion_score).desc())  # optional: 점수 내림차순
            .all()
        )
        return result or []
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

