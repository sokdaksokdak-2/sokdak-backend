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
    - 반환: {emotion_seq: 비율(float)} (1~5 모두 포함)
    """

    # 1~5 감정 미리 초기화
    emotion_score_sums = {seq: 0 for seq in range(1, 6)}
    total_score_sum = 0

    # stats 입력을 바탕으로 감정별 점수 누적
    for item in stats:
        emotion_seq = item[0]
        score_sum_decimal = item[1] # Decimal 타입으로 받은 값을 임시 변수에 저장
        score_sum = float(score_sum_decimal) # float으로 변환

        if isinstance(emotion_seq, int) and isinstance(score_sum, (int, float)):
            if emotion_seq in emotion_score_sums:
                emotion_score_sums[emotion_seq] = score_sum
                total_score_sum += score_sum

    # 총합이 0일 경우, 비율은 전부 0.0
    if total_score_sum == 0:
        return {seq: 0.0 for seq in range(1, 6)}

    # 비율 계산
    return {
        seq: round(score / total_score_sum, 4)
        for seq, score in emotion_score_sums.items()
    }
