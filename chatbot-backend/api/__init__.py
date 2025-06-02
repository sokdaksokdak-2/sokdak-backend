# __init__.py 파일은 패키지의 초기화 파일로, 해당 디렉토리를 패키지로 인식하게 함
# 라우터들을 모아서 FastAPI 애플리케이션에 포함시키는 역할을 함
# chatbot-backend/api/__init__.py

from fastapi import APIRouter

# 각 라우터 import
from .stt_api import router as stt_router
from .emotion_api import router as emotion_router
from .emo_calendar import router as emo_calendar_router
from .emo_report import router as emo_report_router
from .member_api import router as member_router
from .auth_api import router as auth_router
from .oauth_api import router as oauth_router
from .chatbot_api import router as chatbot_router

# APIRouter 인스턴스 생성
api_router = APIRouter()

# 각 라우터들을 버전별로 추가

api_router.include_router(stt_router, prefix="/stt", tags=["stt"])
api_router.include_router(emotion_router, prefix="/emotion", tags=["emotion"])
api_router.include_router(emo_calendar_router, prefix="/emo_calendar", tags=["calendar"])
api_router.include_router(emo_report_router, prefix="/emo_report", tags=["report"])
api_router.include_router(member_router, prefix="/member", tags=["member"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(oauth_router, prefix="/oauth", tags=["OAuth"])
api_router.include_router(chatbot_router, prefix="/chatbot", tags=["chatbot"])

