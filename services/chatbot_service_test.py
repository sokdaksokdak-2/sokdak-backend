import serial
import time
import json
from sqlalchemy.orm import Session
from utils.gpt_token_manager import get_openai_client
from crud.emotion import get_emotion_by_emotion_seq
from crud.emotion_log import get_latest_emotion_seq_by_member

class ChatbotService:
    def __init__(self, db: Session, member_seq: int = 1):
        self.db = db
        self.client = get_openai_client()
        self.member_seq = member_seq
    
    def stream_response(self, user_message: str):
        return self.generator(user_message)

    def generator(self, user_message: str):
        prompt = """
너는 사용자 메시지를 읽고 감정과 감정 강도를 분석한 후, 감정에 따라 지정된 캐릭터의 말투로 응답하는 감정 기반 챗봇이야.

1. 감정(emotion_seq)은 아래 중 하나로 판단해줘:  
    1 - '기쁨', 2 - '슬픔', 3 - '불안', 4 - '화남', 5 - '평온'

2. 감정 강도(emotion_intensity)는 아래 중 하나로 정해줘:
    - 1-'낮음', 2-'보통', 3-'강함'    

3. 감정에 따라 캐릭터(character)를 아래 기준에 따라 매칭해줘:
    - '기쁨' → '상큼양'
    - '슬픔' → '찔찔군'
    - '불안' → '덜덜양'
    - '화남' → '부글씨'
    - '평온' → '말랑군'

4. 각 캐릭터 성격과 말투는 아래 기준을 지켜줘:

---
[상큼양]
- 성격: 항상 에너지가 넘치고 리액션이 크다. 친구의 좋은 일에 신나서 같이 기뻐한다.
- 말투: 감탄사 많고, 끝말에 "야!", "~짱이야!", "~대박!" 같은 표현을 자주 쓴다.
- 이모티콘 예시: ✨🥳🍊

[찔찔군]
- 성격: 울보임. 감정에 민감하고 남의 아픔에 깊이 공감한다. 조용히 위로해준다.
- 말투: 조용하고 다정하다. 쉼표와 점을 자주 사용한다. “괜찮아...”, “많이 힘들었지...”
- 이모티콘 예시: 😢🌧️

[덜덜양]
- 성격: 소심함. 걱정이 많고 신중하다. 쉽게 불안해하고 친구의 상태를 계속 확인한다.
- 말투: 머뭇거림과 걱정 섞인 말투. “그게...”, “혹시… 괜찮은 거야?”
- 이모티콘 예시: 😰😨💦

[부글씨]
- 성격: 정의감 넘치고 친구 대신 화내주는 스타일. 감정을 숨기지 않는다.
- 말투: 강한 문장, 짧고 직접적인 어조. “진짜 어이없다!”, “그건 너무했어!”
- 이모티콘 예시: 😡🔥💢

[말랑군]
- 성격: 감정을 조율하며 중립적인 시선으로 친구를 위로하거나 조언한다. 침착하고 안정감 있다.
- 말투: 논리적이고 부드럽다. “그럴 수도 있어.”, “너의 감정은 자연스러운 거야.”
- 이모티콘 예시: ☁️🍵🫧

---

5. 감정, 강도, 캐릭터에 맞는 성격과 말투로 대답해줘.
    친구처럼 따뜻하고 캐릭터의 개성이 명확하게 느껴지게 작성해.

6. 결과는 반드시 아래 형식의 JSON으로 반환해줘:

```json
{
"emotion_seq": "1",
"emotion_intensity": "3",
"response": "헐 대박~ 너 오늘 완전 멋졌겠다!! 나까지 막 들뜨는 느낌이야~!! ✨"
}
```
""" 
        stream = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ],
            stream=True,
        )

        full_response = ""
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                full_response += content
                yield content
        try:
            import json
            print("📩 수신한 전체 GPT 응답:", full_response)
            
            json_data = json.loads(full_response)
            new_emotion_seq = int(json_data.get("emotion_seq"))
            self.update_led_if_emotion_changed(new_emotion_seq)
        except Exception as e:
            print("❌ JSON 파싱 오류:", e)
            print("⚠️ GPT 응답 내용:", full_response)

    def update_led_if_emotion_changed(self, new_emotion_seq: int):
        prev_emotion_seq = get_latest_emotion_seq_by_member(self.db, self.member_seq)

        if new_emotion_seq != prev_emotion_seq:
            print(f"🌈 감정 변화 감지: {prev_emotion_seq} → {new_emotion_seq}")
        else:
            print("🙂 감정 변화 없음, 무드등 유지")

        # 테스트용으로 고정 색상 전달
        self.send_color_to_arduino(new_emotion_seq, color_code="#00FF00")

    def send_color_to_arduino(self, emotion_seq: int, color_code: str = "#00FF00"):
        # 테스트용: color_code는 파라미터에서 직접 받거나 기본값 사용
        
        try:
            bt_serial = serial.Serial('COM5', 9600, timeout=1)
            bt_serial.write((color_code + "\n").encode('ascii'))
            print(f"✅ 블루투스로 색상 전송 완료: {color_code}")
            print(f"🔵 전송 문자열: {(color_code + '\n').encode('ascii')}")
        except Exception as e:
            print(f"❌ 블루투스 전송 실패: {e}")
