import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:sdsd/config.dart';
import 'package:sdsd/onboarding/intro_screen.dart';
import 'package:sdsd/screen/login_screen.dart';
import 'package:sdsd/screen/settings/feedback_screen.dart';
import 'package:sdsd/screen/settings/nickname_edit_screen.dart';
import 'package:sdsd/screen/settings/notification_setting_screen.dart';
import 'package:sdsd/screen/settings/privacy_policy_screen.dart';
import 'package:sdsd/screen/settings/terms_of_service_screen.dart';
import '../widgets/custom_header.dart';
import 'settings/theme_setting_screen.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).scaffoldBackgroundColor,
      appBar: const CustomHeader(showBackButton: false),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.only(top: 0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const Text(
                '설정',
                style: TextStyle(fontSize: 18, color: Colors.black87),
              ),
              const SizedBox(height: 34),
              Expanded(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _buildCard(
                        context: context,
                        title: '내 정보 관리',
                        items: ['닉네임 변경', '감정 기록 알림 시간 설정', '테마 색상 변경'],
                      ),
                      const SizedBox(height: 12),
                      _buildCard(
                        context: context,
                        title: '앱 정보 및 정책',
                        items: ['서비스 이용약관', '개인정보 처리방침', '의견 보내기 / 도움 요청하기'],
                      ),
                      const SizedBox(height: 12),
                      _buildCard(
                        context: context,
                        title: '계정 관리',
                        items: ['로그아웃', '회원탈퇴'],
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

  Widget _buildCard({
    required BuildContext context,
    required String title,
    required List<String> items,
  }) {
    return Card(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      elevation: 0,
      color: Colors.white,
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 4),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            ListTile(
              dense: true,
              minVerticalPadding: 0,
              contentPadding: const EdgeInsets.symmetric(horizontal: 16),
              leading: _getIconForTitle(title),
              title: Text(
                title,
                style: const TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 17,
                ),
              ),
            ),
            const Divider(height: 0, thickness: 0.8),
            ...items.map(
              (item) => ListTile(
                dense: true,
                minVerticalPadding: 0,
                contentPadding: const EdgeInsets.symmetric(horizontal: 16),
                title: Text(item, style: const TextStyle(fontSize: 16)),
                trailing: const Icon(Icons.chevron_right, size: 18),
                onTap: () {
                  if (item == '회원탈퇴') {
                    _showDeleteAccountDialog(context);
                  } else if (item == '로그아웃') {
                    _showLogoutDialog(context);
                  } else if (item == '테마 색상 변경') {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const ThemeSettingScreen(),
                      ),
                    );
                  } else if (item == '닉네임 변경') {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const NicknameEditScreen(),
                      ),
                    );
                  } else if (item == '감정 기록 알림 시간 설정') {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const NotificationSettingScreen(),
                      ),
                    );
                  } else if (item == '서비스 이용약관') {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const TermsOfServiceScreen(),
                      ),
                    );
                  } else if (item == '개인정보 처리방침') {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const PrivacyPolicyScreen(),
                      ),
                    );
                  } else if (item == '의견 보내기 / 도움 요청하기') {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (_) => const FeedbackScreen()),
                    );
                  }
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showLogoutDialog(BuildContext context) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) {
        return AlertDialog(
          backgroundColor: Colors.white,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
          ),
          contentPadding: EdgeInsets.zero,
          content: SizedBox(
            width: MediaQuery.of(context).size.width * 0.9,
            child: Padding(
              padding: const EdgeInsets.fromLTRB(24, 32, 24, 12),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text(
                    '로그아웃 하시겠습니까?',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 16),
                  ),
                  const SizedBox(height: 24),
                  Row(
                    children: [
                      Expanded(
                        child: SizedBox(
                          height: 40,
                          child: ElevatedButton(
                            onPressed: () => Navigator.pop(context),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.grey[100],
                              foregroundColor: Colors.black,
                              elevation: 0,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(8),
                              ),
                            ),
                            child: const Text('취소'),
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: SizedBox(
                          height: 40,
                          child: ElevatedButton(
                            onPressed: () {
                              Config.accessToken = '';
                              Config.memberSeq = -1;
                              Config.nickname = '';

                              Navigator.pop(context);
                              Navigator.pushAndRemoveUntil(
                                context,
                                MaterialPageRoute(
                                  builder: (_) => const LoginScreen(),
                                ),
                                (route) => false,
                              );
                            },
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.green,
                              foregroundColor: Colors.white,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(8),
                              ),
                            ),
                            child: const Text('확인'),
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                ],
              ),
            ),
          ),
        );
      },
    );
  }

  void _showDeleteAccountDialog(BuildContext context) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) {
        return AlertDialog(
          backgroundColor: Colors.white,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
          ),
          contentPadding: EdgeInsets.zero,
          content: SizedBox(
            width: MediaQuery.of(context).size.width * 0.9,
            child: Padding(
              padding: const EdgeInsets.fromLTRB(24, 32, 24, 12),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text(
                    '모든 감정 기록은 삭제됩니다.\n탈퇴하시겠습니까?',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 16),
                  ),
                  const SizedBox(height: 24),
                  Row(
                    children: [
                      Expanded(
                        child: SizedBox(
                          height: 40,
                          child: ElevatedButton(
                            onPressed: () => Navigator.pop(context),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.grey[100],
                              foregroundColor: Colors.black,
                              elevation: 0,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(8),
                              ),
                            ),
                            child: const Text('취소'),
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: SizedBox(
                          height: 40,
                          child: ElevatedButton(
                            onPressed: () async {
                              Navigator.pop(context);

                              final uri = Uri.parse(
                                '${Config.baseUrl}/api/member/${Config.memberSeq}',
                              );

                              try {
                                final response = await http.delete(
                                  uri,
                                  headers: {
                                    'Content-Type': 'application/json',
                                    'Authorization':
                                        'Bearer ${Config.accessToken}',
                                  },
                                );

                                if (response.statusCode == 200) {
                                  Config.accessToken = '';
                                  Config.memberSeq = -1;
                                  Config.nickname = '';

                                  Navigator.pushAndRemoveUntil(
                                    context,
                                    MaterialPageRoute(
                                      builder: (_) => const IntroScreen(),
                                    ),
                                    (route) => false,
                                  );
                                } else {
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    const SnackBar(
                                      content: Text('회원탈퇴에 실패했어요'),
                                    ),
                                  );
                                }
                              } catch (e) {
                                print('❗ 탈퇴 중 예외 발생: $e');
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(content: Text('서버 오류')),
                                );
                              }
                            },
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.green,
                              foregroundColor: Colors.white,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(8),
                              ),
                            ),
                            child: const Text('확인'),
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                ],
              ),
            ),
          ),
        );
      },
    );
  }

  Icon _getIconForTitle(String title) {
    if (title.contains('내 정보')) return const Icon(Icons.person_outline);
    if (title.contains('앱 정보')) return const Icon(Icons.info_outline);
    if (title.contains('계정')) return const Icon(Icons.logout_outlined);
    return const Icon(Icons.settings);
  }
}
