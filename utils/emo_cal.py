# 한글 감정명을 영어 감정명으로 매핑
emotion_mapping = {
    '기쁨': 'joy',
    '슬픔': 'sadness',
    '분노': 'anger',
    '불안': 'anxiety',
    '평온': 'calm'
}

def calculate_emotion_distribution(stats):
    """
    감정별 (name_kr, emotion_score, count) 리스트를 받아
    영어 감정명 기준 비율 딕셔너리로 변환합니다.
    - stats: [(name_kr, emotion_score, count), ...]
    - 반환: {감정영문명: 비율(float)}
    """
    if not isinstance(stats, list) or not stats:
        return {}

    score_sum = {}
    total = 0

    for item in stats:
        # 잘못된 데이터 방지
        if not isinstance(item, (list, tuple)) or len(item) != 3:
            continue

        name_kr, score, count = item
        eng_name = emotion_mapping.get(name_kr)
        if eng_name and isinstance(score, (int, float)) and isinstance(count, int):
            weighted = score * count
            score_sum[eng_name] = score_sum.get(eng_name, 0) + weighted
            total += weighted

    if total == 0:
        return {}

    return {emotion: round(weight / total, 4) for emotion, weight in score_sum.items()}
