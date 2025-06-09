from sqlalchemy.orm import Session

# def get_latest_emotion_seq_by_member(db: Session, member_seq: int):
#     from models import EmotionCalendarDetail
#     last_entry = (
#         db.query(EmotionCalendarDetail)
#         .filter(EmotionCalendarDetail.member_seq == member_seq)
#         .order_by(EmotionCalendarDetail.created_at.desc())
#         .first()
#     )
#     return last_entry.emotion_seq if last_entry else None


def get_latest_emotion_seq_by_member(db, member_seq: int) -> int | None:
    # 📌 실제 DB 없이 테스트용으로 항상 "중립(5)" 감정이라고 가정
    return 5