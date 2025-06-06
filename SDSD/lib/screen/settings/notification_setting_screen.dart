import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:sdsd/widgets/custom_header.dart';

class NotificationSettingScreen extends StatefulWidget {
  const NotificationSettingScreen({super.key});

  @override
  State<NotificationSettingScreen> createState() =>
      _NotificationSettingScreenState();
}

class _NotificationSettingScreenState extends State<NotificationSettingScreen> {
  bool _isNotificationOn = false;
  TimeOfDay _selectedTime = const TimeOfDay(hour: 20, minute: 0);

  void _onTimeChanged(DateTime newTime) {
    setState(() {
      _selectedTime = TimeOfDay(hour: newTime.hour, minute: newTime.minute);
    });
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
                '알림 시간 설정',
                style: TextStyle(
                  fontSize: 18,
                  // fontWeight: FontWeight.bold,
                  color: Colors.black87,
                ),
              ),
              const SizedBox(height: 34),
              Container(
                margin: const EdgeInsets.symmetric(horizontal: 24),
                padding: const EdgeInsets.symmetric(
                  horizontal: 24,
                  vertical: 20,
                ),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text(
                          '알림 받기',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        CupertinoSwitch(
                          value: _isNotificationOn,
                          onChanged: (value) {
                            setState(() {
                              _isNotificationOn = value;
                            });
                          },
                          activeColor: const Color(0xFF28B960), // 켜졌을 때 색상
                          trackColor: Colors.grey[300], // 꺼졌을 때 배경색
                        ),

                      ],
                    ),
                    if (_isNotificationOn) ...[
                      const SizedBox(height: 20),

                      // ✅ 작은 박스를 중앙 정렬 + 너비 제한
                      Align(
                        alignment: Alignment.center,
                        child: Container(
                          width: 240,
                          padding: const EdgeInsets.symmetric(vertical: 16),
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(16),
                            boxShadow: [
                              BoxShadow(
                                color: Colors.black.withOpacity(0.05),
                                blurRadius: 10,
                                offset: const Offset(0, 4),
                              ),
                            ],
                          ),
                          child: SizedBox(
                            height: 280,
                            child: CupertinoDatePicker(
                              mode: CupertinoDatePickerMode.time,
                              initialDateTime: DateTime(
                                2024,
                                1,
                                1,
                                _selectedTime.hour,
                                _selectedTime.minute,
                              ),
                              use24hFormat: false,
                              onDateTimeChanged: _onTimeChanged,
                            ),
                          ),
                        ),
                      ),

                      const SizedBox(height: 20),

                      // ✅ 안내 문구 (큰 박스 안, 피커 밖)
                      const Text(
                        '감정 기록을 잊지 않도록\n원하는 시간에 알림을 받아보세요.',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          fontSize: 14,
                          color: Colors.black,
                          height: 1.5,
                        ),
                      ),
                    ],
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
