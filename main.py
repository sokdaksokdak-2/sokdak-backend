# main.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from api import api_router
from contextlib import asynccontextmanager
from db import init_db

import logging

logging.basicConfig(
    level=logging.INFO, # INFO 레벨 이상의 로그만 출력(DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - [%(levelname)s] - %(message)s"
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # DB 초기화 (비동기 함수면 await 필요)
    yield
    # 앱 종료 시 cleanup 작업 가능

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://sokdak.kro.kr"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 하나의 api_router로 모든 라우터 묶어서 등록 (단일 진입점)

# 각 라우터를 FastAPI 앱에 포함

app.include_router(api_router, prefix="/api")

# # ✅ 루트 테스트용 경로만 유지
# @app.get("/")
# def root():
#     return {"message": "sokdak api"}
