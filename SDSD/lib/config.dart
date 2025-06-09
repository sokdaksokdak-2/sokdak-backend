// lib/config.dart

class Config {
  // ✅ 개발 중엔 이걸 사용
  static const String baseUrl = 'http://192.168.219.246:8000';
  static int memberSeq = -1; // 로그인 시 저장됨
  static String nickname = '';
  static String accessToken = '';
  static String refreshToken = '';

// 🚀 배포할 땐 여기를 바꿔주면 됨
// static const String baseUrl = 'https://api.mysite.com';
}
