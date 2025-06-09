import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:sdsd/config.dart';
import 'package:sdsd/onboarding/nickname_setup_screen.dart';
import 'package:sdsd/screen/forgot_password_screen.dart';
import 'package:sdsd/screen/home_screen.dart';
import 'package:sdsd/screen/main_screen.dart';
import 'package:sdsd/screen/signup_screen.dart';
import 'package:flutter/gestures.dart';
import 'package:url_launcher/url_launcher.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _obscurePassword = true;

  void _showMessage(String message) {
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(SnackBar(content: Text(message)));
  }

  Future<void> loginUser() async {
    final email = _emailController.text.trim();
    final password = _passwordController.text.trim();

    if (email.isEmpty || password.isEmpty) {
      _showMessage('이메일과 비밀번호를 모두 입력해주세요.');
      return;
    }

    final url = Uri.parse('${Config.baseUrl}/api/auth/login/local');
    final requestBody = jsonEncode({'email': email, 'password': password});

    print('📤 보내는 body: $requestBody');
    print('➡️ 요청 URL: $url');

    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: requestBody,
      );

      print('응답 코드: ${response.statusCode}');
      print('응답 내용: ${response.body}');

      if (response.statusCode == 200) {
        final decoded = utf8.decode(response.bodyBytes);
        final data = jsonDecode(decoded);

        print('✅ 로그인 응답 전체: $data');
        print('👉 member_seq: ${data['member_seq']}');
        print('👉 nickname: ${data['nickname']}');

        final accessToken = data['access_token'];
        final nickname = data['nickname'];
        final memberSeq = data['member_seq'];
        final email = _emailController.text.trim();

        Config.accessToken = accessToken;
        Config.memberSeq = memberSeq;
        Config.nickname = nickname ?? '';

        if (nickname == null || nickname.isEmpty || nickname == email) {
          _showMessage('닉네임을 먼저 설정해주세요!');
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (_) => const NicknameSetupScreen()),
          );
        } else {
          _showMessage('$nickname님, 환영합니다!');
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (_) => const MainScreen()),
          );
        }
      } else if (response.statusCode == 401) {
        _showMessage('비밀번호가 일치하지 않습니다.');
      } else if (response.statusCode == 404) {
        _showMessage('존재하지 않는 이메일입니다.');
      } else if (response.statusCode == 422) {
        final detail = jsonDecode(response.body)['detail'];
        _showMessage('입력 오류: ${detail.toString()}');
      } else {
        _showMessage('알 수 없는 오류 발생: ${response.statusCode}');
      }
    } catch (e) {
      _showMessage('네트워크 오류: $e');
    }
  }

  // 🔗 OAuth 로그인 요청
  void launchOAuth(String provider) async {
    final url = Uri.parse('${Config.baseUrl}/api/oauth/login/$provider');
    if (await canLaunchUrl(url)) {
      await launchUrl(url, mode: LaunchMode.externalApplication);
    } else {
      _showMessage('로그인 페이지를 열 수 없습니다.');
    }
  }

  @override
  Widget build(BuildContext context) {
    final screenHeight = MediaQuery.of(context).size.height;

    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Padding(
                padding: const EdgeInsets.only(top: 8),
                child: InkWell(
                  onTap: () => Navigator.pop(context),
                  borderRadius: BorderRadius.circular(24),
                  child: Container(
                    width: 40,
                    height: 40,
                    decoration: BoxDecoration(
                      color: Colors.white,
                      shape: BoxShape.circle,
                      border: Border.all(color: Colors.grey.shade300),
                    ),
                    child: const Icon(Icons.arrow_back, color: Colors.black),
                  ),
                ),
              ),
              const SizedBox(height: 30),
              const Text(
                '로그인',
                style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 12),
              Expanded(
                child: SingleChildScrollView(
                  child: Column(
                    children: [
                      SizedBox(height: screenHeight * 0.08),
                      TextField(
                        controller: _emailController,
                        decoration: InputDecoration(
                          hintText: '이메일을 입력하세요',
                          hintStyle: const TextStyle(color: Colors.grey),
                          filled: true,
                          fillColor: Colors.grey.shade100,
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(12),
                            borderSide: BorderSide.none,
                          ),
                        ),
                      ),
                      const SizedBox(height: 16),
                      TextField(
                        controller: _passwordController,
                        obscureText: _obscurePassword,
                        decoration: InputDecoration(
                          hintText: '비밀번호를 입력하세요',
                          hintStyle: const TextStyle(color: Colors.grey),
                          filled: true,
                          fillColor: Colors.grey.shade100,
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(12),
                            borderSide: BorderSide.none,
                          ),
                          suffixIcon: IconButton(
                            icon: Icon(
                              _obscurePassword
                                  ? Icons.visibility_off
                                  : Icons.visibility,
                            ),
                            onPressed: () {
                              setState(() {
                                _obscurePassword = !_obscurePassword;
                              });
                            },
                          ),
                        ),
                      ),
                      const SizedBox(height: 8),
                      Align(
                        alignment: Alignment.centerRight,
                        child: TextButton(
                          onPressed: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder:
                                    (context) => const ForgotPasswordScreen(),
                              ),
                            );
                          },
                          child: const Text(
                            '비밀번호 찾기',
                            style: TextStyle(
                              fontSize: 14,
                              color: Colors.grey,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 8),
                      SizedBox(
                        width: double.infinity,
                        height: 50,
                        child: ElevatedButton(
                          onPressed: loginUser,
                          style: ElevatedButton.styleFrom(
                            backgroundColor: const Color(0xFF28B960),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                          ),
                          child: const Text(
                            '로그인',
                            style: TextStyle(
                              fontSize: 15,
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 16),
                      const Center(child: Text('또는')),
                      const SizedBox(height: 16),

                      // ✅ 카카오
                      SizedBox(
                        width: double.infinity,
                        height: 50,
                        child: ElevatedButton.icon(
                          onPressed: () => launchOAuth('kakao'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.yellow,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                            elevation: 0,
                          ),
                          icon: Image.asset(
                            'assets/images/kakao_icon.png',
                            height: 20,
                            width: 20,
                          ),
                          label: const Text(
                            '카카오톡으로 계속하기',
                            style: TextStyle(
                              fontSize: 14,
                              color: Colors.black,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 12),

                      // ✅ Google
                      SizedBox(
                        width: double.infinity,
                        height: 50,
                        child: OutlinedButton.icon(
                          onPressed: () => launchOAuth('google'),
                          style: OutlinedButton.styleFrom(
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                          ),
                          icon: Image.asset(
                            'assets/images/google_icon.png',
                            height: 20,
                            width: 20,
                          ),
                          label: const Text(
                            'Google로 계속하기',
                            style: TextStyle(
                              fontSize: 14,
                              color: Colors.black,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 12),

                      // ✅ Naver
                      SizedBox(
                        width: double.infinity,
                        height: 50,
                        child: ElevatedButton.icon(
                          onPressed: () => launchOAuth('naver'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.black,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                          ),
                          icon: Image.asset(
                            'assets/images/naver_icon.png',
                            height: 20,
                            width: 20,
                          ),
                          label: const Text(
                            'Naver로 계속하기',
                            style: TextStyle(
                              fontSize: 14,
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ),

                      const SizedBox(height: 24),
                      Center(
                        child: RichText(
                          text: TextSpan(
                            style: const TextStyle(
                              fontSize: 13,
                              color: Color(0xFF282828),
                            ),
                            children: [
                              const TextSpan(text: '가입한 계정이 없으신가요? '),
                              TextSpan(
                                text: '시작하기',
                                style: const TextStyle(
                                  fontSize: 13,
                                  color: Color(0xFF45D3E3),
                                  fontWeight: FontWeight.bold,
                                ),
                                recognizer:
                                    TapGestureRecognizer()
                                      ..onTap = () {
                                        Navigator.push(
                                          context,
                                          MaterialPageRoute(
                                            builder:
                                                (context) =>
                                                    const SignupScreen(),
                                          ),
                                        );
                                      },
                              ),
                            ],
                          ),
                        ),
                      ),
                      const SizedBox(height: 24),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
