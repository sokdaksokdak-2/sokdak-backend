import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:sdsd/providers/theme_provider.dart';
import '../../widgets/custom_header.dart';

class ThemeSettingScreen extends StatefulWidget {
  const ThemeSettingScreen({super.key});

  @override
  State<ThemeSettingScreen> createState() => _ThemeSettingScreenState();
}

class _ThemeSettingScreenState extends State<ThemeSettingScreen> {
  final List<Map<String, dynamic>> themes = [
    {
      'name': '크림 베이지',
      'color': Color(0xFFFFF0E0),
      'code': '#FFF0E0',
      'description': '따뜻하고 포근',
    },
    {
      'name': '라이트 민트',
      'color': Color(0xFFDFF9F3),
      'code': '#E9F7F3',
      'description': '상쾌하고 안정적',
    },
    {
      'name': '소프트 라벤더',
      'color': Color(0xFFF3F0FF),
      'code': '#F3F0FF',
      'description': '정서적 안정감',
    },
    {
      'name': '파스텔 피치',
      'color': Color(0xFFFFEFE6),
      'code': '#FFEFE6',
      'description': '다정하고 감성적',
    },
    {
      'name': '연그레이 블루',
      'color': Color(0xFFF0F4F8),
      'code': '#F0F4F8',
      'description': '신뢰감, 차분한 톤',
    },
  ];

  int selectedIndex = 3;

  @override
  void initState() {
    super.initState();
    final currentThemeColor =
        Provider.of<ThemeProvider>(context, listen: false).themeColor;

    final index = themes.indexWhere(
          (theme) => theme['color'] == currentThemeColor,
    );

    if (index != -1) {
      selectedIndex = index;
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
                '테마 색상 변경',
                style: TextStyle(fontSize: 18, color: Colors.black87),
              ),
              const SizedBox(height: 34),
              Expanded(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  child: Column(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(16),
                          color: Colors.white,
                        ),
                        child: Column(
                          children: [
                            const Text(
                              '앱의 분위기를 내 취향대로 바꿔보세요.',
                              style: TextStyle(fontSize: 16),
                            ),
                            const SizedBox(height: 16),
                            Container(
                              height: 60,
                              width: double.infinity,
                              decoration: BoxDecoration(
                                color: themes[selectedIndex]['color'],
                                borderRadius: BorderRadius.circular(12),
                                border: Border.all(color: Colors.grey.shade300),
                              ),
                              alignment: Alignment.center,
                              child: Text(
                                '미리보기\n${themes[selectedIndex]['code']}',
                                textAlign: TextAlign.center,
                                style: const TextStyle(
                                  fontSize: 16,
                                  color: Colors.black87,
                                ),
                              ),
                            ),
                            const SizedBox(height: 20),
                            const Align(
                              alignment: Alignment.centerLeft,
                              child: Text(
                                '원하는 테마를 선택하세요',
                                style: TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                            ),
                            const SizedBox(height: 16),
                            GridView.builder(
                              shrinkWrap: true,
                              physics: const NeverScrollableScrollPhysics(),
                              itemCount: themes.length,
                              gridDelegate:
                              const SliverGridDelegateWithFixedCrossAxisCount(
                                crossAxisCount: 2,
                                crossAxisSpacing: 16,
                                mainAxisSpacing: 12,
                                childAspectRatio: 1.45,
                              ),
                              itemBuilder: (context, index) {
                                final theme = themes[index];
                                final isSelected = selectedIndex == index;

                                return GestureDetector(
                                  onTap: () => setState(() => selectedIndex = index),
                                  child: Container(
                                    padding: const EdgeInsets.fromLTRB(12, 12, 12, 2),
                                    decoration: BoxDecoration(
                                      color: Colors.white,
                                      borderRadius: BorderRadius.circular(16),
                                      border: Border.all(
                                        color: isSelected
                                            ? Colors.black87
                                            : Colors.grey.shade300,
                                        width: isSelected ? 2 : 1,
                                      ),
                                    ),
                                    child: Column(
                                      mainAxisAlignment: MainAxisAlignment.start,
                                      crossAxisAlignment: CrossAxisAlignment.center,
                                      children: [
                                        Stack(
                                          alignment: Alignment.center,
                                          children: [
                                            CircleAvatar(
                                              radius: 24,
                                              backgroundColor: theme['color'],
                                            ),
                                            if (isSelected)
                                              const Icon(
                                                Icons.check,
                                                size: 25,
                                                color: Colors.black87,
                                              ),
                                          ],
                                        ),
                                        const SizedBox(height: 6),
                                        Text(
                                          theme['name'] ?? '',
                                          style: const TextStyle(
                                            fontSize: 12,
                                            fontWeight: FontWeight.bold,
                                          ),
                                        ),
                                        const SizedBox(height: 1),
                                        Text(
                                          theme['description'] ?? '',
                                          textAlign: TextAlign.center,
                                          maxLines: 2,
                                          style: const TextStyle(
                                            fontSize: 10,
                                            color: Colors.black54,
                                            height: 1.2,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                );
                              },
                            ),
                            const SizedBox(height: 12),
                            Row(
                              children: [
                                Expanded(
                                  child: ElevatedButton(
                                    onPressed: () => Navigator.pop(context),
                                    style: ElevatedButton.styleFrom(
                                      backgroundColor: Colors.grey[200],
                                      foregroundColor: Colors.black87,
                                      elevation: 0,
                                      shape: RoundedRectangleBorder(
                                        borderRadius: BorderRadius.circular(10),
                                      ),
                                    ),
                                    child: const Text('취소'),
                                  ),
                                ),
                                const SizedBox(width: 12),
                                Expanded(
                                  child: ElevatedButton(
                                    onPressed: () {
                                      final selectedColor =
                                      themes[selectedIndex]['color'] as Color;

                                      Provider.of<ThemeProvider>(
                                        context,
                                        listen: false,
                                      ).setTheme(selectedColor);

                                      ScaffoldMessenger.of(context).showSnackBar(
                                        SnackBar(
                                          behavior: SnackBarBehavior.floating,
                                          backgroundColor: Colors.grey[500],
                                          elevation: 6,
                                          shape: RoundedRectangleBorder(
                                            borderRadius:
                                            BorderRadius.circular(12),
                                          ),
                                          margin: const EdgeInsets.symmetric(
                                            horizontal: 24,
                                            vertical: 16,
                                          ),
                                          duration: const Duration(seconds: 2),
                                          content: Row(
                                            children: [
                                              const CircleAvatar(
                                                radius: 12,
                                                backgroundColor: Color(0xFF28B960),
                                                child: Icon(
                                                  Icons.check,
                                                  size: 20,
                                                  color: Colors.white,
                                                ),
                                              ),
                                              const SizedBox(width: 12),
                                              const Expanded(
                                                child: Text(
                                                  '테마가 적용되었습니다!',
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
                                    },
                                    style: ElevatedButton.styleFrom(
                                      backgroundColor: Colors.green,
                                      foregroundColor: Colors.white,
                                      shape: RoundedRectangleBorder(
                                        borderRadius: BorderRadius.circular(10),
                                      ),
                                    ),
                                    child: const Text('적용하기'),
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 12),
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
