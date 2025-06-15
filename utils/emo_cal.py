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
    감정별 (emotion_seq, emotion_score, count) 리스트를 받아
    emotion_seq 기준 비율 딕셔너리로 변환합니다.
    - stats: [(emotion_seq, emotion_score, count), ...]
    - 반환: {emotion_seq: 비율(float)}
    """
    if not isinstance(stats, list) or not stats:
        return {}

    score_sum = {}
    total = 0

    for item in stats:
        if not isinstance(item, (list, tuple)) or len(item) != 3:
            continue

        emotion_seq, score, count = item
        if isinstance(emotion_seq, int) and isinstance(score, (int, float)) and isinstance(count, int):
            weighted = score * count
            score_sum[emotion_seq] = score_sum.get(emotion_seq, 0) + weighted
            total += weighted

    if total == 0:
        return {}

    return {emotion_seq: round(weight / total, 4) for emotion_seq, weight in score_sum.items()}