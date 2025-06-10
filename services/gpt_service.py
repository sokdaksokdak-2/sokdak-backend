import openai
import json
from utils import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

# 감정 분석용 프롬프트 생성
def generate_emotion_prompt(raw_text: str) -> str:
    return f"""
    당신의 역할은 감정 분석가 입니다.

    다음 텍스트를 읽고 화자의 감정을 분석하세요.
    - 감정은 다음 중 하나여야 합니다:
    - joy (기쁨), sadness (슬픔), anger (분노), anxiety (불안), calm (평온)
    - 감정 강도는 1 (약함), 2 (보통), 3 (강함) 중 하나로 판단하세요.

    다음 JSON 형식으로 출력하세요:
    {{"emotion_name_en": "감정영문명", "emotion_score": 숫자}}

    예시:
    {{"emotion_name_en": "joy", "emotion_score": 2}}

    텍스트:
    \"\"\"{raw_text}\"\"\"
    """

# 감정 분석 실행 함수
def analyze_emotion_from_text(raw_text: str) -> dict:
    prompt = generate_emotion_prompt(raw_text)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        answer = response.choices[0].message["content"].strip()
        emotion_data = json.loads(answer)
        return emotion_data

    except Exception as e:
        print("감정 분석 중 오류 발생:", e)
        return {
            "emotion_name_en": "unknown",
            "emotion_score": 0
        }

# GPT를 활용한 월간 감정 요약
def generate_monthly_summary(contexts: list[str]) -> str:
    joined_text = "\n".join(contexts)
    prompt = f"""
    당신의 역할은 감정 분석가입니다.
    
    다음은 사용자가 한 달 동안 작성한 감정 메모들입니다. 이 메모들을 바탕으로 사용자의 감정 흐름을 중심으로 3~4문장으로 요약해 주세요.

    - 주로 어떤 감정이 자주 나타났는지
    - 감정에 영향을 준 주요 사건 또는 상황이 있었는지
    - 전반적인 심리 상태는 어떤지
    - 위 내용에 대해 공감 및 피드백

    {joined_text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message['content']
