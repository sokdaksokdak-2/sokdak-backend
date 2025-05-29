from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# 환경변수에서 API 키 불러오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY가 .env 파일에 정의되어 있지 않습니다.")
