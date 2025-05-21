from fastapi import FastAPI
from api import api_router
from contextlib import asynccontextmanager
from db.init_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # init_db가 동기 함수라면 이렇게
    init_db()
    # 만약 init_db가 async라면: await init_db()
    yield
    # 여기서 정리 작업 가능

app = FastAPI(lifespan=lifespan)

# 각 라우터를 FastAPI 앱에 포함
app.include_router(api_router, prefix="/api", tags=["stt"])


@app.get("/")
async def root():
    return {"message": "chatbot api"}

