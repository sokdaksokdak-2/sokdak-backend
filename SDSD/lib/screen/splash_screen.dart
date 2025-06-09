import 'package:flutter/material.dart';
import 'package:sdsd/config.dart';
import 'package:sdsd/screen/login_screen.dart';
import 'package:sdsd/screen/main_screen.dart';
import 'package:sdsd/utils/deeplink_handler.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  bool _deeplinkHandled = false;

  @override
  void initState() {
    super.initState();
    _initializeApp();
  }

  Future<void> _initializeApp() async {
    // ✅ 1. 딥링크 우선 처리 시도
    await handleInitialLink(context);
    _deeplinkHandled = true;

    // ✅ 2. 딥링크로 처리되지 않았고, 이미 로그인된 유저라면 MainScreen
    if (mounted &&
        Config.accessToken.isNotEmpty &&
        Config.memberSeq != -1 &&
        _deeplinkHandled) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const MainScreen()),
      );
    } else {
      // ✅ 3. 로그인 필요
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const LoginScreen()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      backgroundColor: Colors.white,
      body: Center(
        child: CircularProgressIndicator(), // 로딩 중
      ),
    );
  }
}
