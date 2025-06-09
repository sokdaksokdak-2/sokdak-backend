import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:provider/provider.dart';
import 'package:app_links/app_links.dart'; // ✅ 변경

import 'package:sdsd/onboarding/intro_screen.dart';
import 'package:sdsd/onboarding/nickname_setup_screen.dart';
import 'package:sdsd/providers/theme_provider.dart';
import 'package:sdsd/screen/main_screen.dart';
import 'package:sdsd/config.dart';

void main() {
  runApp(
    ChangeNotifierProvider(
      create: (_) => ThemeProvider(),
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final AppLinks _appLinks = AppLinks(); // ✅ app_links 인스턴스
  StreamSubscription<Uri>? _sub;
  Widget _currentScreen = const IntroScreen();

  @override
  void initState() {
    super.initState();
    _initDeepLinks();
  }

  Future<void> _initDeepLinks() async {
    try {
      // 초기 링크 처리
      final initialUri = await _appLinks.getInitialAppLink();
      if (initialUri != null) _onDeepLink(initialUri);

      // 스트림 리스닝
      _sub = _appLinks.uriLinkStream.listen((uri) {
        if (uri != null) _onDeepLink(uri);
      });
    } catch (e) {
      print('딥링크 처리 중 오류 발생: $e');
    }
  }

  Future<void> _onDeepLink(Uri uri) async {
    if (uri.scheme == 'myapp' &&
        uri.host == 'oauth' &&
        uri.path == '/callback') {
      final accessToken = uri.queryParameters['access_token'];
      final refreshToken = uri.queryParameters['refresh_token'];
      final nickname = uri.queryParameters['nickname'];
      final memberSeq = int.tryParse(uri.queryParameters['member_seq'] ?? '');

      if (accessToken != null && memberSeq != null) {
        Config.accessToken = accessToken;
        Config.refreshToken = refreshToken ?? '';
        Config.nickname = nickname ?? '';
        Config.memberSeq = memberSeq;

        final needsNickname = nickname == null || nickname.isEmpty;

        setState(() {
          _currentScreen =
          needsNickname ? const NicknameSetupScreen() : const MainScreen();
        });
      }
    }
  }

  @override
  void dispose() {
    _sub?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final themeColor = Provider.of<ThemeProvider>(context).themeColor;

    return MaterialApp(
      debugShowCheckedModeBanner: false,
      locale: const Locale('ko', 'KR'),
      supportedLocales: const [Locale('en', 'US'), Locale('ko', 'KR')],
      localizationsDelegates: GlobalMaterialLocalizations.delegates,
      theme: ThemeData(
        scaffoldBackgroundColor: themeColor,
        appBarTheme: AppBarTheme(backgroundColor: themeColor),
        bottomNavigationBarTheme: BottomNavigationBarThemeData(
          backgroundColor: themeColor,
        ),
      ),
      home: _currentScreen,
    );
  }
}
