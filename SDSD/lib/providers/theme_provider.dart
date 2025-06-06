import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ThemeProvider with ChangeNotifier {
  Color _themeColor = const Color(0xFFFFEFE6); // 기본 테마 (파스텔 피치)

  Color get themeColor => _themeColor;

  ThemeProvider() {
    _loadThemeFromPrefs(); // 앱 시작 시 테마 불러오기
  }

  void setTheme(Color color) {
    _themeColor = color;
    _saveThemeToPrefs();
    notifyListeners();
  }

  void _loadThemeFromPrefs() async {
    final prefs = await SharedPreferences.getInstance();
    final colorHex = prefs.getString('theme_color');
    if (colorHex != null) {
      _themeColor = Color(int.parse(colorHex));
      notifyListeners();
    }
  }

  void _saveThemeToPrefs() async {
    final prefs = await SharedPreferences.getInstance();
    prefs.setString('theme_color', _themeColor.value.toString());
  }
}
