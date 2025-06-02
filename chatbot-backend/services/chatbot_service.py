from sqlalchemy.orm import Session
from utils.gpt import analyze_emotion_from_text
from utils.gpt_token_manager import get_openai_client
from crud.emotion import get_emotion_by_emotion_seq

client = get_openai_client()

class ChatbotService:
    def __init__(self, db: Session):
        self.db = db
        self.client = get_openai_client()

    def stream_response(self, prompt: str):
        def generator():
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "너는 사용자에게 10년 된 친구처럼 대화해줘."},
                    {"role": "user", "content": prompt}
                ],
                stream=True,
            )
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content

        return generator()
    
    
    
