# core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str

    openai_api_key: str
    google_client_id:str
    google_client_secret:str
    google_redirect_uri:str

    kakao_client_id:str
    kakao_redirect_uri:str

    naver_client_id:str
    naver_client_secret:str
    naver_redirect_uri:str

    jwt_secret_key:str
    jwt_algorithm:str = "HS256"

    vito_client_id:str
    vito_client_secret:str
    vito_auth_url:str

    redis_host: str
    redis_port : int
    redis_db : int
    redis_password : str | None = None


    class Config:
        env_file = ".env"

settings = Settings()
