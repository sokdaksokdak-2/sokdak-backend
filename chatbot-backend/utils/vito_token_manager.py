import time
import requests
from fastapi import HTTPException

CLIENT_ID = "aahd2L5mbJjItwYY9Khf"
CLIENT_SECRET = "HxKZe8oQeNNXg3cd8cpxQctfh0w-1mOp4-ZdfrZa"
AUTH_URL = "https://openapi.vito.ai/v1/authenticate"

access_token = None
expire_at = 0

def get_new_token():
    global access_token, expire_at

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(AUTH_URL, data=data, headers=headers)
    if response.status_code == 200:
        resp_json = response.json()
        access_token = resp_json.get("access_token")
        expire_at = resp_json.get("expire_at")
        print(f"새 토큰 발급 완료. 만료시간: {expire_at}")
    else:
        raise HTTPException(status_code=500, detail="토큰 발급 실패")

def get_valid_token():
    now = int(time.time())
    if not access_token or expire_at - now < 300:
        get_new_token()
    return access_token
