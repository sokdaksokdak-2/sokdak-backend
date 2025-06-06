from fastapi import HTTPException
from sqlalchemy.orm import Session
from utils import get_openai_client, redis_client
import json
from schemas.chatbot import ChatHistoryDto, ChatHistoryDto01
from prompts.prompts import CHAT_PROMPT, EMOTION_ANALYSIS_PROMPT
from datetime import datetime
from core.emotion_config import EMOTION_NAME_MAP, STRENGTH_MAP
from crud import emo_calendar as emo_calendar_crud
from collections import Counter
import logging
from typing import AsyncGenerator
import asyncio
from utils.redis_client import redis_client
from services.emo_arduino_service import ArduinoService


REDIS_CHAT_HISTORY_KEY = "chat_history:{}"
HISTORY_LIMIT = 3 # 최근 대화 내역 저장 개수

logger = logging. getLogger(__name__)
client = get_openai_client()

class ChatbotService:
    def __init__(self, redis_client: redis_client, db: Session, member_seq: int): # , member_seq: int 이것도임 ㅇㅇ
        self.db = db
        self.member_seq = member_seq  # 우현- 추가한거 나중에 삭제하던가
        self.client = get_openai_client()
        self.redis_client = redis_client  # 이거도 우현 추가한거

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
            "emotion_intensity": 2
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



    # 이 아래로 우현이가 추가한 코드 ㅇㅇ
    from schemas.chatbot import ChatHistoryDto01
    async def stream_response(self, user_message: str) -> AsyncGenerator[str, None]:
        """
        사용자 메시지에 대해 GPT 모델로부터 스트리밍 응답을 생성 및 저장
        """
        # 1. 최근 대화 불러오기
        chat_history = await self.get_chat_history(self.member_seq, HISTORY_LIMIT)

        # 2. 프롬프트 구성
        prompt = self.build_chatbot_prompt_test_(user_message, chat_history)

        # 3. OpenAI 스트리밍 호출
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=prompt,
            temperature=1.0,
            stream=True,
        )

        # 4. 스트리밍 응답 yield
        full_response = ""
        for chunk in response:
            delta = chunk.choices[0].delta
            if hasattr(delta, "content") and delta.content:
                content = delta.content
                full_response += content
                yield f"data: {content}\n\n"
            await asyncio.sleep(0)

        # 5. 감정 분석
        emotion_prompt = self.build_emotion_prompt(user_message)
        emotion_result = await self.call_openai(emotion_prompt, model="gpt-3.5-turbo", temperature=0.3)

        # 초기값 설정
        emotion_seq = 1
        emotion_score = 1

        try:
            emotion_data = json.loads(emotion_result)
            emotion_seq = emotion_data.get("emotion_seq") or 1
            emotion_score = emotion_data.get("emotion_intensity") or 1
        except json.JSONDecodeError as e:
            logger.warning(f"감정 분석 실패: {e}")

        # 아두이노 감정 변화 전송
        try:
            arduino_service = ArduinoService(self.db)
            await arduino_service.detect_and_send_emotion_change(
                member_seq=self.member_seq,
                current_emotion_seq=emotion_seq  # ✅ None 방지됨
            )
        except Exception as e:
            logger.warning(f"아두이노 전송 실패: {e}")

        # Redis 저장
        try:
            chatbot_response_json = {
                "response": full_response.strip(),
                "emotion_seq": emotion_seq,
                "emotion_score": emotion_score
            }

            await self.save_chat_history(
                self.member_seq,
                ChatHistoryDto01(
                    user_message=user_message,
                    chatbot_response=chatbot_response_json,
                    created_at=datetime.now(),
                )
            )
        except Exception as e:
            logger.warning(f"스트리밍 응답 저장 중 예외 발생: {e}")

    async def save_chat_history(self, member_seq: int, recode: ChatHistoryDto01):
        key = f"chat_history:{member_seq}"
        recode_dict = recode.model_dump()

        # datetime을 문자열로 변환
        recode_dict["created_at"] = recode_dict["created_at"].isoformat()

        # ✅ 여기에 이중 직렬화 방지 코드 추가
        if isinstance(recode_dict.get("chatbot_response"), dict):
            pass  # dict라면 OK
        elif isinstance(recode_dict.get("chatbot_response"), str):
            try:
                recode_dict["chatbot_response"] = json.loads(recode_dict["chatbot_response"])
            except Exception:
                logger.warning("chatbot_response가 dict 아님. 그대로 저장.")

        # Redis에 저장
        await self.redis_client.lpush(key, json.dumps(recode_dict))
        await self.redis_client.ltrim(key, 0, HISTORY_LIMIT - 1)
    
    async def get_chat_history(self, member_seq: int, limit: int = 5) -> list[ChatHistoryDto]:
        key = f"chat_history:{member_seq}"
        raw_history = await self.redis_client.lrange(key, 0, limit - 1)

        history = []
        for item in raw_history:
            parsed = json.loads(item)

            # ✅ chatbot_response가 문자열이면 dict로 파싱
            if isinstance(parsed.get("chatbot_response"), str):
                try:
                    parsed["chatbot_response"] = json.loads(parsed["chatbot_response"])
                except json.JSONDecodeError:
                    logger.warning("chatbot_response JSON 파싱 실패")

            # ✅ created_at을 datetime으로 변환
            if isinstance(parsed.get("created_at"), str):
                parsed["created_at"] = datetime.fromisoformat(parsed["created_at"])

            # ✅ Pydantic DTO로 파싱
            try:
                history.append(ChatHistoryDto(**parsed))
            except Exception as e:
                logger.warning(f"ChatHistoryDto 파싱 실패: {e} / 데이터: {parsed}")

        return list(reversed(history))


    def build_chatbot_prompt_test_(self, user_message: str, chat_history: list[ChatHistoryDto] | None = None):
        '''
        챗봇 응답 생성
        '''
        prompt = [{"role": "system", "content": CHAT_PROMPT}]

        for record in chat_history:
            # 🔒 안전한 chatbot_response 파싱
            response = record.chatbot_response
            if isinstance(response, str):
                try:
                    response = json.loads(response)
                except json.JSONDecodeError:
                    logger.warning(f"chatbot_response 디코딩 실패: {response}")
                    response = {}
            elif not isinstance(response, dict):
                logger.warning("chatbot_response가 dict가 아님. 기본값 사용.")
                response = {}

            # 안전하게 값 추출
            emotion_seq = response.get("emotion_seq")
            emotion_score = response.get("emotion_score")

            # 감정명과 강도 매핑
            emotion_name = EMOTION_NAME_MAP.get(emotion_seq, "알 수 없음")
            emotion_strength = STRENGTH_MAP.get(emotion_score, "알 수 없음")

            # 프롬프트 구성
            prompt.append({"role": "user", "content": f"{record.user_message} (감정: {emotion_name}, 강도: {emotion_strength})"})
            prompt.append({"role": "assistant", "content": json.dumps(response, ensure_ascii=False)})
            logger.info(f"{record}")

        prompt.append({"role": "user", "content": user_message})
        return prompt