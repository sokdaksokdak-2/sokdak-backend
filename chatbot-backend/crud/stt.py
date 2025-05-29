import openai
from sqlalchemy.orm import Session
from models import EmotionCalendar, EmotionCalendarDetail
from utils import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

# 텍스트를 GPT API로 요약하고 context 필드에 저장
def summarize_and_store_stt_text(db: Session, member_seq: int, calendar_seq: int, text: str) -> str:
    # calendar_seq와 member_seq가 유효한지 확인
    calendar = db.query(EmotionCalendar).filter(
        EmotionCalendar.calendar_seq == calendar_seq,
        EmotionCalendar.member_seq == member_seq
    ).first()
    if not calendar:
        raise ValueError("해당 calendar_seq가 존재하지 않거나, 회원 정보가 일치하지 않습니다.")

    # GPT 요약 요청
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "다음 사용자의 음성 인식 텍스트를 간결하게 요약해 주세요."},
                {"role": "user", "content": text}
            ],
            temperature=0.7
        )
        summary_text = response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"GPT 요약 중 오류 발생: {str(e)}")

    # 가장 최근의 EmotionCalendarDetail에 저장
    detail = db.query(EmotionCalendarDetail)\
        .filter(EmotionCalendarDetail.calendar_seq == calendar_seq)\
        .order_by(EmotionCalendarDetail.created_at.desc())\
        .first()
    if not detail:
        raise ValueError("해당 calendar_seq에 대한 EmotionCalendarDetail 레코드가 없습니다.")

    detail.context = summary_text
    db.commit()

    return summary_text

# 저장된 context 필드 값 조회
def get_context_by_calendar_seq(db: Session, calendar_seq: int) -> str | None:
    detail = db.query(EmotionCalendarDetail)\
        .filter(EmotionCalendarDetail.calendar_seq == calendar_seq)\
        .order_by(EmotionCalendarDetail.created_at.desc())\
        .first()
    return detail.context if detail else None
