class EmotionRecord {
  final int? seq; // ✅ optional, 새로 만들 땐 null일 수도 있음
  final String emotion;
  final String title;
  final String content;
  // final String intensity; // ✅ 추가됨: 약함 / 보통 / 강함 중 하나

  EmotionRecord({
    this.seq,
    required this.emotion,
    required this.title,
    required this.content,
    // required this.intensity,
  });
}
