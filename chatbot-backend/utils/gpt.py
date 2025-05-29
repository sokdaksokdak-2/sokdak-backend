import openai
from utils import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

# 감정 분석용 프롬프트 생성
def generate_emotion_prompt(raw_text: str) -> str:
    return f"""
다음 텍스트를 읽고 화자의 감정을 분석하세요. 감정은 다음 중 하나여야 합니다:
- joy (기쁨)
- sadness (슬픔)
- anger (분노)
- anxiety (불안)
- calm (평온)

감정 강도는 1 (약함), 2 (보통), 3 (강함) 중 하나로 판단해주세요.

다음 JSON 형식으로 출력해주세요:
{{"emotion_name_en": "감정", "emotion_intensity": 강도}}

예: {{"emotion_name_en": "joy", "emotion_intensity": 2}}

텍스트:
\"\"\"{raw_text}\"\"\"
"""

# 감정 분석 실행 함수
def analyze_emotion_from_text(raw_text: str) -> dict:
    prompt = generate_emotion_prompt(raw_text)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        answer = response.choices[0].message["content"].strip()
        # 문자열에서 JSON 파싱 시도
        import json
        emotion_data = json.loads(answer)
        return emotion_data

    except Exception as e:
        print("감정 분석 중 오류 발생:", e)
        return {
            "emotion_name_en": "unknown",
            "emotion_intensity": 0
        }
