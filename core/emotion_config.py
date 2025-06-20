# emotion_config.py
"""
감정 관련 상수 파일
계속 쿼리로 조회하는건 비효율적이라 판단, 상수로 정의
""" 

EMOTION_NAME_MAP = {
    1: "기쁨",
    2: "슬픔",
    3: "불안",
    4: "분노",
    5: "중립"
}

CHARACTER_MAP = {
    1: "상큼양",
    2: "찔찔군",
    3: "덜덜양",
    4: "부글씨",
    5: "말랑군"
}

STRENGTH_MAP = {
    1: "낮음",
    2: "보통",
    3: "강함"
}

EMOTION_COLOR_MAP = {
    1: "#FDC420",  # 기쁨 (joy)
    2: "#4a7edf",  # 슬픔 (sadness)
    3: "#FC5F15",  # 불안 (anxiety)
    4: "#be2d35",  # 화남 (anger)
    5: "#8ED465",  # 평온 (neutral)
}