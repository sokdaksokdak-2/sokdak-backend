from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from db.session import get_session
from services.chatbot_service_test import ChatbotService
from schemas.chatbot import StreamingChatRequestDto
import logging
import time

logger = logging.getLogger(__name__)


router = APIRouter()

@router.post("/stream",
             summary="openai 스트리밍 챗봇 대화",
              response_model=None)
async def stream_chat(request: StreamingChatRequestDto, db: Session = Depends(get_session)):
    start_time = time.time()
    logger.info(f"챗봇 API 호출 시작: {round(start_time ,3)}초")


    chatbot_service = ChatbotService(db)
    generator = chatbot_service.stream_response(request.user_message)

    logger.info(f"챗봇 API 호출 종료: {round(time.time() - start_time, 3)}초")

    return StreamingResponse(generator, media_type="text/event-stream")


@router.post("/stream_test",
             summary="openai 스트리밍 챗봇 대화",
              response_model=None)
async def stream_chat_test(request: StreamingChatRequestDto, db: Session = Depends(get_session)):
    start_time = time.time()
    logger.info(f"챗봇 API 호출 시작: {round(start_time ,3)}초")


    chatbot_service = ChatbotService(db=db, member_seq=request.member_seq)
    generator = chatbot_service.stream_response(request.user_message)

    logger.info(f"챗봇 API 호출 종료: {round(time.time() - start_time, 3)}초")

    return StreamingResponse(generator, media_type="text/event-stream")