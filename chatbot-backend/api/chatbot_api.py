from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from db.session import get_session
from services.chatbot_service import ChatbotService
from schemas.chatbot import StreamingChatRequestDto


router = APIRouter()

@router.post("/stream", response_model=None)
async def stream_chat(request: StreamingChatRequestDto, db: Session = Depends(get_session)):


    chatbot_service = ChatbotService(db)
    generator = chatbot_service.stream_response(request.user_message)

    return StreamingResponse(generator, media_type="text/event-stream")
