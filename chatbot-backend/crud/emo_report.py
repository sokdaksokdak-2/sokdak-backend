from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from models import EmotionCalendarDetail, EmotionCalendar, Emotion, EmotionReport
from datetime import date, timedelta
from typing import Dict
import openai
from utils import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

# 감정 시퀀스를 영어 이름으로 매핑 (기본 감정 5개)
emotion_mapping = {
    '기쁨': 'joy',
    '슬픔': 'sadness',
    '분노': 'anger',
    '불안': 'anxiety',
    '평온': 'calm'
}

# 전달 월의 감정 데이터를 계산하여 파이차트용 분포를 생성
def calculate_emotion_distribution(db: Session, member_seq: int, target_month: date) -> Dict[str, float]:
    # 전달의 시작과 끝 날짜
    start_date = (target_month.replace(day=1) - timedelta(days=1)).replace(day=1)
    end_date = target_month.replace(day=1) - timedelta(days=1)

    # 감정 캘린더와 디테일, 감정 테이블을 조인해서 감정별로 count
    results = db.query(
        Emotion.name_kr,
        Emotion.emotion_intensity,
        func.count().label("count")
    ).join(EmotionCalendar, EmotionCalendar.calendar_seq == EmotionCalendarDetail.calendar_seq
    ).join(Emotion, Emotion.emotion_seq == EmotionCalendarDetail.emotion_seq
    ).filter(
        EmotionCalendar.member_seq == member_seq,
        EmotionCalendar.calendar_date >= start_date,
        EmotionCalendar.calendar_date <= end_date
    ).group_by(Emotion.name_kr, Emotion.emotion_intensity).all()

    # 감정별 가중합 계산
    score_sum = {}
    total = 0

    for name_kr, score, count in results:
        eng_name = emotion_mapping.get(name_kr)
        if eng_name:
            weighted = score * count
            score_sum[eng_name] = score_sum.get(eng_name, 0) + weighted
            total += weighted

    # 비율 계산 (전체 가중합 대비 각 감정의 비율)
    distribution = {emotion: round(weight / total, 4) for emotion, weight in score_sum.items()}
    return distribution

# GPT API를 활용하여 전달 메모 내용을 요약
def generate_monthly_summary(contexts: list[str]) -> str:
    joined_text = "\n".join(contexts)
    prompt = f"""
    다음은 한 달간 사용자가 작성한 감정 메모입니다. 이 내용을 3~4문장으로 요약해 주세요.

    {joined_text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message['content']

# 전체 요약 처리
def create_emotion_report(db: Session, member_seq: int, today: date):
    target_month = today  # ex. 2025-06-01이면 5월 리포트

    # 1. 전달 감정 비율 계산
    distribution = calculate_emotion_distribution(db, member_seq, target_month)

    # 2. 전달 context 수집
    start_date = (target_month.replace(day=1) - timedelta(days=1)).replace(day=1)
    end_date = target_month.replace(day=1) - timedelta(days=1)

    contexts = db.query(EmotionCalendarDetail.context
    ).join(EmotionCalendar, EmotionCalendar.calendar_seq == EmotionCalendarDetail.calendar_seq
    ).filter(
        EmotionCalendar.member_seq == member_seq,
        EmotionCalendar.calendar_date >= start_date,
        EmotionCalendar.calendar_date <= end_date,
        EmotionCalendarDetail.context.isnot(None)
    ).all()

    context_texts = [c[0] for c in contexts if c[0]]

    # 3. GPT 요약
    summary_text = generate_monthly_summary(context_texts) if context_texts else None

    # 4. DB 저장
    new_report = EmotionReport(
        report_date=start_date,
        emotion_distribution=distribution,
        summary_text=summary_text,
        created_at=today,
        member_seq=member_seq
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report

# 특정 회원의 특정 달 리포트 조회 함수
def get_emotion_report(db: Session, member_seq: int, report_month: date):
    # report_month에서 해당 월의 1일로 맞추기 (예: 2025-05-15 → 2025-05-01)
    month_start = report_month.replace(day=1)

    return db.query(EmotionReport).filter(
        EmotionReport.member_seq == member_seq,
        EmotionReport.report_date == month_start
    ).first()