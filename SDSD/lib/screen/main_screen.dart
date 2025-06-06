import 'package:flutter/material.dart';
import 'package:sdsd/screen/calendar_screen.dart';
import 'package:sdsd/screen/home_screen.dart';
import 'package:sdsd/screen/mission_suggest_screen.dart';
import 'package:sdsd/screen/report_screen.dart';
import 'package:sdsd/screen/settings_screen.dart';

class MainScreen extends StatefulWidget {
  final int initialIndex;

  const MainScreen({super.key, this.initialIndex = 2});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  late int _selectedIndex;
  late List<Widget> _screens; // ✅ late 선언

  @override
  void initState() {
    super.initState();
    _selectedIndex = widget.initialIndex;

    _screens = const [
      CalendarScreen(),              // ✅ 감정 캘린더 연결됨
      ReportScreen(),
      HomeScreen(),
      MissionSuggestScreen(),
      SettingsScreen(),
    ];
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        type: BottomNavigationBarType.fixed,
        backgroundColor: Colors.white,
        selectedItemColor: Colors.black,
        unselectedItemColor: Colors.grey.shade400,
        onTap: (index) {
          setState(() {
            _selectedIndex = index;
          });
        },
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.calendar_month), label: '캘린더'),
          BottomNavigationBarItem(icon: Icon(Icons.description_outlined), label: '리포트'),
          BottomNavigationBarItem(icon: Icon(Icons.home), label: '홈'),
          BottomNavigationBarItem(icon: Icon(Icons.track_changes_outlined), label: '미션'),
          BottomNavigationBarItem(icon: Icon(Icons.settings), label: '설정'),
        ],
      ),
    );
  }
}
