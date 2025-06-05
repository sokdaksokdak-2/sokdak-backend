from fastapi import HTTPException
from sqlalchemy.orm import Session
from utils.gpt_token_manager import get_openai_client
from utils.redis_client import redis_client
import json
from schemas.chatbot import ChatHistoryDto
from prompts.prompts import CHAT_PROMPT, EMOTION_ANALYSIS_PROMPT
from datetime import datetime
from core.emotion_config import EMOTION_NAME_MAP, STRENGTH_MAP
from crud import emo_calendar as emo_calendar_crud
from collections import Counter
import logging

REDIS_CHAT_HISTORY_KEY = "chat_history:{}"
HISTORY_LIMIT = 3 # 최근 대화 내역 저장 개수

logger = logging. getLogger(__name__)
client = get_openai_client()

class ChatbotService:
    def __init__(self, db: Session):
        self.db = db
        self.client = get_openai_client()

    # 1. 사용자 대화 분석 -> 감정 분류
    # 2. 감정 분류에 따른 대화 스크립트 생성
    # 3. DB 저장
    # 4. 사용자 응답
    # TODO : 대화 내역 가져오기
    async def get_chat_history(self, member_seq: int, limit: int = None) -> list[ChatHistoryDto]:
        '''
            Redis에서 대화 내역 가져오기
            - limit이 None이면 전체 내역 반환
            - limit이 양수면 최근 limit개 반환
        '''

        key = REDIS_CHAT_HISTORY_KEY.format(member_seq)

        if limit is None:
            chat_history = await redis_client.lrange(key, 0, -1)
        else:
            chat_history = await redis_client.lrange(key, -limit, -1)

        chat_history_list = [ChatHistoryDto(**json.loads(history)) for history in chat_history]

        for item in chat_history_list:
            logger.info(f"{item}")
        return chat_history_list
        
    # TODO : 대화 내용 요약 저장 수정
    async def save_chat_summary(self, member_seq: int):
        '''대화 종료 후 대화 내용 요약 저장
        '''
        key = REDIS_CHAT_HISTORY_KEY.format(member_seq)
        chat_history = self.get_chat_history(member_seq)

        if chat_history is None:
            return

        # 사용자 메시지, 감정, 감정강도 만 가져와서 Title, summary, 가장 크게 느낀 감정 추출
        user_messages = []
        emotion_list = []
        emotion_score_list = []
        for item in chat_history:
            user_message = item.get("user_message")
            emotion_seq = item.get("emotion_seq")
            emotion_score = item.get("strength")

            if user_message and emotion_seq and emotion_score:
                user_messages.append(f"{user_message} (감정: {emotion_seq}, 강도: {emotion_score})")
                emotion_list.append(emotion_seq)
                emotion_score_list.append(emotion_score)

        # 대화 내용 요약, 감정
        summary_prompt = self.build_summary_prompt(user_messages)
        summary = await self.call_openai(summary_prompt, "gpt-3.5-turbor") 
        title = summary.get("title")
        context = summary.get("context")

        # 가장 많이 등장한 감정을 기준으로 대표 정하기
        most_common_emotion_seq = Counter(emotion_list).most_common(1)[0][0]
        avg_emotion_score = round(sum(emotion_score_list) / len(emotion_score_list), 1)

        await emo_calendar_crud.save_emotion_calender(
            self.db,
            member_seq,
            most_common_emotion_seq,
            avg_emotion_score,
            title,
            context,
            "ai"
        )

        await redis_client.delete(key)
        
    async def save_chat_history(self, member_seq: int, recode: ChatHistoryDto):
        '''사용자 상태 저장 - 현재 대화 내역
        # Key : chat_history:{member_seq}
        # Value (JSON 문자열)
        {
            "user_message": "오늘 진짜 너무 힘들었어...",
            "bot_response": "괜찮아... 정말 많이 힘들었겠구나. 내가 곁에 있어줄게... 😢🌧️",
            "emotion": "2",
            "strength": "3",
            "timestamp": 1717482053.1252
        }
        '''
        key = REDIS_CHAT_HISTORY_KEY.format(member_seq)
        
        # json 형식으로 value 저장
        recode_json = recode.model_dump_json()
        await redis_client.rpush(key, recode_json)
        # await redis_client.ltrim(key, -HISTORY_LIMIT, -1)

        logger.info(f"💬 대화 내역 저장 : {recode_json}")
        
    def build_emotion_prompt(self, user_message: str):
        '''사용자 메시지에 따른 감정 분류
        JSON 형식으로 반환
        {
            "emotion_seq": 1,
            "strength": 2
        }
        '''
        return [
            {"role": "system", "content": EMOTION_ANALYSIS_PROMPT},
            {"role": "user", "content": user_message}
        ]


    def build_chatbot_prompt(self,user_message: str, chat_history: list[ChatHistoryDto] | None = None):
        '''
        챗봇 응답 생성
        '''
        prompt = [{"role": "system", "content": CHAT_PROMPT}]
    
        for record in chat_history:
            prompt.append({"role": "user", "content": f"{record.user_message} (감정: {EMOTION_NAME_MAP[record.chatbot_response.get('emotion_seq')]}, 강도: {STRENGTH_MAP[record.chatbot_response.get('emotion_score')]})"})
            prompt.append({"role": "assistant", "content": json.dumps(record.chatbot_response, ensure_ascii=False)})
            logger.info(f"{record}")
        
        prompt.append({"role": "user", "content": user_message})
        return prompt
        
    
    async def get_chatbot_response(self, member_seq: int, user_message: str):
        # 1. 최근 대화 내역 가져오기
        chat_history = await self.get_chat_history(member_seq, HISTORY_LIMIT)
        # 2. 감정 분류 - 현재 대화
        # emotion_analysis_prompt = self.build_emotion_prompt(user_message)
        # emotion_response = await self.call_openai(model="gpt-3.5-turbo", prompt=emotion_analysis_prompt)
        
        # try :
        #     emotion_response = json.loads(emotion_response)
        # except json.JSONDecodeError as e:
        #     logger.error(f"감정 분석 실패: {e}")
        #     raise HTTPException(status_code=500, detail="감정 분석 실패")
        
        # logger.info(f"🚨최근 대화 내역 결과 : {chat_history}")
        # 3. 챗봇 응답 생성 string
        chatbot_prompt = self.build_chatbot_prompt(user_message, chat_history)
        chatbot_response = await self.call_openai(prompt=chatbot_prompt, model="gpt-4o-mini")
        logger.info(chatbot_response)

        try: 
            chatbot_response_json = json.loads(chatbot_response)
            # 대화 내역 저장 -redis
            await self.save_chat_history(
                    member_seq, 
                    ChatHistoryDto(
                        user_message=user_message,
                        chatbot_response=chatbot_response_json,
                        created_at=datetime.now(),
                    ),
                )
        except json.JSONDecodeError as e:
            # JSON 파싱 실패 시 에러 로그 출력
            logger.error(f"챗봇 응답 JSON 파싱 실패: {e}")
            raise HTTPException(status_code=500, detail="챗봇 응답 JSON 파싱 실패")

            

        return chatbot_response_json
    
    # GPT 모델 호출
    async def call_openai(self, prompt: str, model: str = "gpt-3.5-turbor", temperature: float = 1.0):
        response = client.chat.completions.create(
            model=model,
            messages=prompt,
            temperature=temperature,
            stream=False,
        )
        return response.choices[0].message.content

    async def get_chatbot_response_no_user(self, user_message: str, model: str = "gpt-3.5-turbo"):
        '''비회원용 대화 응답 (히스토리 저장 안 함)'''
        
        if not user_message.strip():
            raise ValueError("user_message cannot be empty")

        prompt = [
            {"role": "system", "content": CHAT_PROMPT},
            {"role": "user", "content": user_message}
        ]

        response =await self.call_openai(prompt, model)
        response_json = json.loads(response)

        
        return response_json.get("response")


    
