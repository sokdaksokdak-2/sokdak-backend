import 'package:flutter/material.dart';
import 'package:app_links/app_links.dart';
import 'package:sdsd/config.dart';
import 'package:sdsd/screen/main_screen.dart';

Future<void> handleInitialLink(BuildContext context) async {
  final appLinks = AppLinks();

  try {
    final uri = await appLinks.getInitialAppLink();

    if (uri != null &&
        uri.scheme == 'myapp' &&
        uri.host == 'oauth' &&
        uri.path == '/callback') {
      final accessToken = uri.queryParameters['access_token'];
      final refreshToken = uri.queryParameters['refresh_token'];
      final nickname = uri.queryParameters['nickname'];
      final memberSeq = uri.queryParameters['member_seq'];

      if (accessToken != null) {
        Config.accessToken = accessToken;
        Config.refreshToken = refreshToken ?? '';
        Config.nickname = nickname ?? '';
        Config.memberSeq = int.tryParse(memberSeq ?? '-1') ?? -1;

        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => const MainScreen()),
        );
      }
    }
  } catch (e) {
    print('❌ 딥링크 처리 오류: $e');
  }
}
