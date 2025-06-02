from core.config import settings
from openai import OpenAI

# 환경변수에서 API 키 불러오기
OPENAI_API_KEY = settings.openai_api_key

def get_openai_client():
    if OPENAI_API_KEY is None:
        raise ValueError("OPENAI_API_KEY가 .env 파일에 정의되어 있지 않습니다.")

    return OpenAI(api_key=OPENAI_API_KEY)

