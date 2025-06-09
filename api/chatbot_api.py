from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from db.session import get_session
from services.chatbot_service import ChatbotService
# from services.mission_service import MissionService
from schemas.chatbot import StreamingChatRequestDto, ChatRequestDto, ChatHistoryDto
import logging
import time
from datetime import datetime
from utils.redis_client import get_redis
from redis.asyncio import Redis             # 이 두개도 추가한거 우현

logger = logging.getLogger(__name__)


router = APIRouter()

# DI 주입 방식으로 변경
# TODO : 이후 dependencies/auth_dependencies.py 파일로 분리
def get_chatbot_service(db: Session = Depends(get_session)) -> ChatbotService:
    return ChatbotService(db)

# def get_mission_service(db: Session = Depends(get_session)) -> MissionService:
#     return MissionService(db)


# 앱 첫 실행시에는 상큼이 출현, 이후 대화에서는 분석 결과에 따라 캐릭터 변경
# 앱 실행 시 유저 있는지 확인 후 없으면 상큼이 출현

@router.post("/chat",
             summary="챗봇 대화 - 이전 대화 반영 ",
             )
async def chat_message(request: ChatRequestDto, chatbot_service: ChatbotService = Depends(get_chatbot_service)):
    start_time = time.time()
    logger.info(f"✅챗봇 API 호출 시작: {round(start_time ,3)}초")
                                             
    if not request.member_seq or not request.user_message:
        raise HTTPException(status_code=400, detail="member_seq 또는 user_message가 없습니다.")
    
    response = await chatbot_service.get_chatbot_response(request.member_seq, request.user_message)

    logger.info(f"챗봇 API 호출 종료: {round(time.time() - start_time, 3)}초")

    return response


# @router.post("/chat/summary/{member_seq}",
#                 summary="대화 종료 후 챗봇 내용 요약",
#                 status_code=200,
#             )
# async def chat_summary(member_seq: int,chatbot_service: ChatbotService = Depends(get_chatbot_service)):
#     return await chatbot_service.save_chat_diary(member_seq)

# @router.post("/chat/complete/{member_seq}",
#                 summary="대화 종료 후 챗봇 내용 요약 및 미션생성",
#                 status_code=200,
#             )
# async def complete_chat_session(member_seq: int,
#                                 chatbot_service: ChatbotService = Depends(get_chatbot_service),
#                                 mission_service: MissionService = Depends(get_mission_service),
#                                 background_tasks: BackgroundTasks = Depends()):
#     chat_history = await chatbot_service.get_chat_history(member_seq)
    
#     mission = await mission_service.create_mission(member_seq, chat_history)

#     background_tasks.add_task(chatbot_service.save_chat_diary, member_seq, chat_history)
#     background_tasks.add_task(chatbot_service.delete_chat_history, member_seq)
#     logger.info(f"대화 종료 후 챗봇 내용 요약 및 미션 생성 완료 : {mission}")
    
#     return mission


@router.post("/stream",
             summary="챗봇 대화 - 이전 대화 기억 못함",
            response_model=None)
async def stream_chat(request: StreamingChatRequestDto, chatbot_service: ChatbotService = Depends(get_chatbot_service)):
    start_time = time.time()
    logger.info(f"챗봇 API 호출 시작: {round(start_time ,3)}초")

    response = await chatbot_service.get_chatbot_response_no_user(request.user_message)

    logger.info(f"챗봇 API 호출 종료: {round(time.time() - start_time, 3)}초")
    return response


@router.post("/stream_test",
             summary="챗봇 아두이노 테스트",
              response_model=None)
async def stream_chat_test(request: StreamingChatRequestDto, db: Session = Depends(get_session), redis_client: Redis = Depends(get_redis)):
    start_time = time.time()
    logger.info(f"챗봇 API 호출 시작: {round(start_time ,3)}초")


    chatbot_service = ChatbotService(db=db, member_seq=request.member_seq, redis_client=redis_client)

    generator = chatbot_service.stream_response(request.user_message)

    logger.info(f"챗봇 API 호출 종료: {round(time.time() - start_time, 3)}초")

    return StreamingResponse(generator, media_type="text/event-stream")

