import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:sdsd/config.dart';
import 'package:sdsd/screen/main_screen.dart';

class NicknameSetupScreen extends StatefulWidget {
  const NicknameSetupScreen({super.key});

  @override
  State<NicknameSetupScreen> createState() => _NicknameSetupScreenState();
}

class _NicknameSetupScreenState extends State<NicknameSetupScreen> {
  final TextEditingController _nicknameController = TextEditingController();
  bool _isLoading = false;

  void _showMessage(String message) {
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(SnackBar(content: Text(message)));
  }

  Future<void> _submitNickname() async {
    final nickname = _nicknameController.text.trim();

    if (nickname.isEmpty) {
      _showMessage('닉네임을 입력해주세요.');
      return;
    }

    if (Config.memberSeq == -1) {
      _showMessage('로그인 정보가 없습니다. 다시 로그인해주세요.');
      return;
    }

    setState(() => _isLoading = true);

    final url = Uri.parse('${Config.baseUrl}/api/member/nickname');

    try {
      final response = await http.put(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'member_seq': Config.memberSeq,
          'nickname': nickname,
        }),
      );

      setState(() => _isLoading = false);

      if (response.statusCode == 200) {
        Config.nickname = nickname;
        _showMessage('닉네임 설정 완료!');
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => const MainScreen(initialIndex: 2)),
        );
      } else {
        _showMessage('닉네임 설정 실패: ${response.statusCode}');
      }
    } catch (e) {
      setState(() => _isLoading = false);
      _showMessage('오류 발생: $e');
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
              const SizedBox(height: 8),
              InkWell(
                onTap: () => Navigator.pop(context),
                borderRadius: BorderRadius.circular(24),
                child: Container(
                  width: 40,
                  height: 40,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    border: Border.all(color: Colors.grey.shade300),
                  ),
                  child: const Icon(Icons.arrow_back, color: Colors.black),
                ),
              ),
              const SizedBox(height: 30),
              const Text(
                '내 닉네임 설정하기',
                style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              const Text(
                '우리 더 가까워지기 전에,\n이름부터 알려줄래?',
                style: TextStyle(fontSize: 16, color: Colors.grey),
              ),
              const SizedBox(height: 32),
              TextField(
                controller: _nicknameController,
                decoration: InputDecoration(
                  hintText: '소곤이',
                  hintStyle: const TextStyle(color: Colors.grey),
                  filled: true,
                  fillColor: Colors.grey.shade100,
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide: BorderSide.none,
                  ),
                ),
              ),
              const SizedBox(height: 36),
              SizedBox(
                width: double.infinity,
                height: 50,
                child: ElevatedButton(
                  onPressed: _isLoading ? null : _submitNickname,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF28B960),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child:
                      _isLoading
                          ? const CircularProgressIndicator(color: Colors.white)
                          : const Text(
                            '다음',
                            style: TextStyle(
                              fontSize: 15,
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                            ),
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
