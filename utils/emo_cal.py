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
    감정별 (emotion_seq, score_sum, count) 리스트를 받아
    emotion_seq 기준 score_sum(가중치 합산) 비율 딕셔너리로 변환합니다.
    - stats: [(emotion_seq, score_sum, count), ...]
    - 반환: {emotion_seq: 비율(float)}
    """
    if not isinstance(stats, list) or not stats:
        return {}

    score_sum_dict = {}
    total = 0

    for item in stats:
        if not isinstance(item, (list, tuple)) or len(item) < 2:
            continue
        emotion_seq = item[0]
        score_sum = item[1]
        if isinstance(emotion_seq, int) and isinstance(score_sum, (int, float)):
            score_sum_dict[emotion_seq] = score_sum
            total += score_sum

    if total == 0:
        return {}

    return {emotion_seq: round(score / total, 4) for emotion_seq, score in score_sum_dict.items()}