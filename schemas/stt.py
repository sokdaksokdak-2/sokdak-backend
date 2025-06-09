from pydantic import BaseModel
from typing import Optional

# 클라이언트에서 요약 요청 시 사용하는 요청 모델
class STTRequest(BaseModel):
    member_seq: int
    calendar_seq: int
    text: str

# 요약 결과를 반환할 응답 모델
class STTResponse(BaseModel):
    calendar_seq: int
    context: str

# 저장된 context 값을 응답하는 모델
class ContextResponse(BaseModel):
    calendar_seq: int
    context: Optional[str]