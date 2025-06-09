from fastapi import HTTPException
from sqlalchemy.orm import Session
from utils import get_openai_client, redis_client
import json

from schemas.chatbot import ChatHistoryDto
from prompts.prompts import CHAT_PROMPT, EMOTION_ANALYSIS_PROMPT, CHAT_HISTORY_SUMMARY_PROMPT

from datetime import datetime
from core.emotion_config import EMOTION_NAME_MAP, STRENGTH_MAP
from crud import emo_calendar
from collections import Counter
import logging
from typing import AsyncGenerator
import asyncio
from services.emo_arduino_service import ArduinoService

# from services.mission_service import mission_service


REDIS_CHAT_HISTORY_KEY = "chat_history:{}"
HISTORY_LIMIT = 3 # 최근 대화 내역 저장 개수


logger = logging.getLogger(__name__)
client = get_openai_client()

class ChatbotService:
    def __init__(self, db: Session): 
        self.db = db
        self.client = get_openai_client()
        self.redis_client = redis_client  # Redis 클라이언트 인스턴스 - 우현 추가
        # self.mission_service = mission_service


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

        # for item in chat_history_list:
        #     logger.info(f"{item}")
        return chat_history_list
        

    # TODO : 대화 내용 요약 저장 수정
    async def save_chat_diary(self, member_seq: int):
        '''대화 종료 후 대화 내용 요약 저장
        '''
        key = REDIS_CHAT_HISTORY_KEY.format(member_seq)
        chat_history = await self.get_chat_history(member_seq)


        if not chat_history:
            logger.info(f"[{member_seq}] 저장할 대화 내용이 없습니다.")
            return

        # 사용자 메시지, 감정, 감정강도 만 가져와서 Title, summary, 가장 크게 느낀 감정 추출
        user_messages = []
        emotion_list = []
        emotion_score_list = []
        for item in chat_history:
            user_message = item.user_message
            emotion_seq = item.chatbot_response.get("emotion_seq")
            emotion_score = item.chatbot_response.get("emotion_score")

            if user_message and emotion_seq and emotion_score:
                user_messages.append(f"{user_message} (감정: {emotion_seq}, 강도: {emotion_score})")
                emotion_list.append(emotion_seq)
                emotion_score_list.append(emotion_score)

        logger.info(user_messages)
        logger.info(emotion_list)
        logger.info(emotion_score_list)



        # 대화 내용 요약, 감정 - openai 호출
        diary_prompt = self.build_diary_prompt(chat_history)
        diary = await self.call_openai(diary_prompt, "gpt-4o-mini")
        logger.info(f"응답 : {diary}")
        diary_json = json.loads(diary)
        title = diary_json.get("title")
        context = diary_json.get("diary")
        most_common_emotion_seq = diary_json.get("emotion_seq")
        avg_emotion_score = diary_json.get("emotion_score")

        # 가장 많이 등장한 감정을 기준으로 대표 정하기 -> GPT가 다 해줌ㅎ;;
        # Counter(emotion_list) -> {1: 3, 2: 2, 3: 1} 각 값이 몇 번 등장했는지 세어주는 딕셔너리 반환됨
        # .most_common(1) -> [(1, 3)] 가장 많이 등장한 감정과 그 횟수 반환
        # most_common_emotion_seq = Counter(emotion_list).most_common(1)[0][0]
        # avg_emotion_score = round(sum(emotion_score_list) / len(emotion_score_list), 0)

        # logger.info(f"가장 많이 등장한 감정 : {most_common_emotion_seq}, 평균 감정 강도 : {avg_emotion_score}")

        logger.info(f"대화 요약 저장 - 제목: {title}, 내용: {context}, 감정: {most_common_emotion_seq}, 평균 감정 강도: {avg_emotion_score}")

        try :
            emo_calendar.save_emotion_calendar(
                self.db,
                member_seq,
                most_common_emotion_seq,
                avg_emotion_score,
                title,
                context,
                "ai"
            )


        except Exception as e:
            logger.error(f"대화 요약 저장 실패 : {e}")
            raise HTTPException(status_code=500, detail="대화 요약 저장 실패")
        
             
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

    # TODO : redis 관련 로직들 분리 할지 고민..
    def delete_chat_history(self, member_seq: int):
        '''사용자 상태 삭제 - 현재 대화 내역
        '''
        key = REDIS_CHAT_HISTORY_KEY.format(member_seq)
        redis_client.delete(key)
        logger.info(f"💬 대화 내역 삭제 : {key}")


    def build_emotion_prompt(self, user_message: str):
        '''사용자 메시지에 따른 감정 분류
        JSON 형식으로 반환
        {
            "emotion_seq": 1,
            "emotion_intensity": 2
        }
        '''
        return [
            {"role": "system", "content": EMOTION_ANALYSIS_PROMPT},
            {"role": "user", "content": user_message}
        ]

    # 사용자가 말한것만 포함
    def build_diary_prompt(self, chat_history: list[ChatHistoryDto]):
        '''사용자 메시지에 따른 대화 내용 요약
        JSON 형식으로 반환
        {
            "title": "오늘의 대화 요약",
            "context": "오늘은 정말 힘든 하루였어요..."
        }
        '''
        
        user_message_list = []
        for record in chat_history:
            if record.user_message:
                emotion_seq = EMOTION_NAME_MAP[record.chatbot_response.get('emotion_seq')]
                emotion_score = STRENGTH_MAP[record.chatbot_response.get('emotion_score')]
                msg = f"{record.user_message} (감정: {emotion_seq}, 강도: {emotion_score})"
                user_message_list.append(msg)
        user_messages = "\n".join(user_message_list)

        prompt = [{"role": "system", "content": CHAT_HISTORY_SUMMARY_PROMPT.format(user_messages=user_messages)}]

        # 이부분에 어떻게 대화 넣을지
        for record in chat_history:
            prompt.append({"role": "user", "content": f"{record.user_message} (감정: {EMOTION_NAME_MAP[record.chatbot_response.get('emotion_seq')]}, 강도: {STRENGTH_MAP[record.chatbot_response.get('emotion_score')]})"})

        # logger.info(f"대화 요약 프롬프트 생성 - {prompt}")
        return prompt
        
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

        # 2. 챗봇 응답 생성 json
        chatbot_prompt = self.build_chatbot_prompt(user_message, chat_history)
        chatbot_response = await self.call_openai(prompt=chatbot_prompt, model="gpt-4o-mini")
        logger.info(chatbot_response)

        try: 
            chatbot_response_json = json.loads(chatbot_response)
            # 대화 내역 저장 - redis
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

    
    async def send_emotion_to_arduino_if_changed(
            self,
            member_seq: int,
            current_emotion_seq: int,
        ):
            # 최근 대화 내역에서 이전 감정 seq 가져오기
            chat_history = await self.get_chat_history(member_seq, limit=2)
            previous_emotion_seq = None
            if chat_history:
                last_response = chat_history[-2].chatbot_response
                if last_response:
                    previous_emotion_seq = last_response.get("emotion_seq")
            else:
                # 대화가 1개 밖에 없으면 그걸 이전 감정으로 간주
                last_response = chat_history[-1].chatbot_response
                if last_response:
                    previous_emotion_seq = last_response.get("emotion_seq")

              # 로그 출력
            logger.info(f"[Arduino] 이전 감정 seq: {previous_emotion_seq}, 현재 감정 seq: {current_emotion_seq}")

            arduino_service = ArduinoService(self.db)

            await arduino_service.send_color_if_emotion_changed(
                member_seq=member_seq,
                current_emotion_seq=current_emotion_seq,
                previous_emotion_seq=previous_emotion_seq,
            )

    async def test_get_latest_chat_history(self, member_seq: int):
        key = REDIS_CHAT_HISTORY_KEY.format(member_seq)
        # 최근 1개를 가져옴
        chat_history = await redis_client.lrange(key, 0, -2)  # -1부터 -1까지, 가장 마지막 아이템 1개
        if not chat_history:
            logger.info("채팅 내역 없음")
            return None

        # Redis에서 가져온 값은 바이트 문자열일 수 있으니 디코딩 필요하면 decode()
        latest_history_json = chat_history[0]
        if isinstance(latest_history_json, bytes):
            latest_history_json = latest_history_json.decode('utf-8')

        latest_chat = ChatHistoryDto(**json.loads(latest_history_json))
        logger.info(f"최신 대화 내역: {latest_chat}")
        return latest_chat

