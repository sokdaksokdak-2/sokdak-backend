import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import '../../widgets/custom_header.dart';
import '../../config.dart';

class NicknameEditScreen extends StatefulWidget {
  const NicknameEditScreen({super.key});

  @override
  State<NicknameEditScreen> createState() => _NicknameEditScreenState();
}

class _NicknameEditScreenState extends State<NicknameEditScreen> {
  final TextEditingController _myNicknameController = TextEditingController();
  String currentMyNickname = '';

  @override
  void initState() {
    super.initState();
    currentMyNickname = Config.nickname; // ✅ 닉네임 직접 할당
  }

  Future<void> updateNickname() async {
    final newNickname = _myNicknameController.text.trim();

    // 유효성 검사
    if (newNickname.isEmpty ||
        newNickname.length < 2 ||
        newNickname.length > 10) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text('닉네임은 2~10자로 입력해주세요')));
      return;
    }

    final nicknameReg = RegExp(r'^[a-zA-Z0-9가-힣]+$');
    if (!nicknameReg.hasMatch(newNickname)) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text('한글, 영어, 숫자만 사용할 수 있어요')));
      return;
    }

    final uri = Uri.parse('${Config.baseUrl}/api/member/nickname');

    try {
      final response = await http.put(
        uri,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ${Config.accessToken}',
        },
        body: jsonEncode({
          'member_seq': Config.memberSeq,
          'nickname': newNickname,
        }),
      );

      if (response.statusCode == 200) {
        // final changed = utf8.decode(response.bodyBytes).replaceAll('"', '');
        final changed = newNickname;

        setState(() {
          currentMyNickname = changed;
          _myNicknameController.clear();
        });

        Config.nickname = changed; // ✅ Config에도 반영

        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            behavior: SnackBarBehavior.floating,
            backgroundColor: Colors.grey[500],
            elevation: 6,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
            margin: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
            duration: const Duration(seconds: 2),
            content: Row(
              children: [
                CircleAvatar(
                  radius: 12,
                  backgroundColor: const Color(0xFF28B960),
                  child: const Icon(Icons.check, size: 20, color: Colors.white),
                ),
                const SizedBox(width: 12),
                const Expanded(
                  child: Text(
                    '닉네임이 변경되었습니다.',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 15,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ),
              ],
            ),
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('닉네임 변경 실패: ${response.statusCode}')),
        );
      }
    } catch (e) {
      print('❗ 예외 발생: $e');
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text('서버 연결 실패')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).scaffoldBackgroundColor,
      appBar: const CustomHeader(showBackButton: true),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.only(top: 0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const Text(
                '닉네임 변경',
                style: TextStyle(fontSize: 18, color: Colors.black87),
              ),
              const SizedBox(height: 34),
              Expanded(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  child: Column(
                    children: [
                      Card(
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(16),
                        ),
                        elevation: 0,
                        color: Colors.white,
                        child: Padding(
                          padding: const EdgeInsets.fromLTRB(16, 16, 16, 20),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                '현재 닉네임: ${currentMyNickname.isNotEmpty ? currentMyNickname : '불러오는 중...'}',
                                style: const TextStyle(fontSize: 16),
                              ),
                              const SizedBox(height: 12),
                              TextField(
                                controller: _myNicknameController,
                                decoration: InputDecoration(
                                  hintText: '새 닉네임 입력',
                                  hintStyle: const TextStyle(
                                    fontSize: 16,
                                    color: Colors.grey,
                                  ),
                                  contentPadding: const EdgeInsets.symmetric(
                                    horizontal: 12,
                                    vertical: 14,
                                  ),
                                  enabledBorder: OutlineInputBorder(
                                    borderSide: BorderSide(
                                      color: Colors.grey.shade300,
                                    ),
                                    borderRadius: BorderRadius.circular(15),
                                  ),
                                  focusedBorder: OutlineInputBorder(
                                    borderSide: BorderSide(
                                      color: Colors.grey.shade400,
                                    ),
                                    borderRadius: BorderRadius.circular(15),
                                  ),
                                ),
                              ),
                              const SizedBox(height: 12),
                              Align(
                                alignment: Alignment.centerRight,
                                child: SizedBox(
                                  height: 40,
                                  child: ElevatedButton(
                                    onPressed: updateNickname,
                                    style: ElevatedButton.styleFrom(
                                      backgroundColor: const Color(0xFF28B960),
                                      foregroundColor: Colors.white,
                                      padding: const EdgeInsets.symmetric(
                                        horizontal: 28,
                                      ),
                                      shape: RoundedRectangleBorder(
                                        borderRadius: BorderRadius.circular(8),
                                      ),
                                    ),
                                    child: const Text(
                                      '변경',
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                      const SizedBox(height: 12),
                      const Center(
                        child: Text(
                          '※ 닉네임은 2~10자, 한글/영문/숫자만 가능',
                          textAlign: TextAlign.center,
                          style: TextStyle(fontSize: 14, color: Colors.black),
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
