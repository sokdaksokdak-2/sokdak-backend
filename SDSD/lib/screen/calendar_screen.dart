import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:table_calendar/table_calendar.dart';
import '../widgets/custom_header.dart';
import '../models/emotion_record.dart';
import '../widgets/emotion_input_dialog.dart';
import '../widgets/emotion_record_viewer_dialog.dart';
import '../widgets/emotion_from_text_dialog.dart';
import 'package:sdsd/services/emotion_service.dart';

class CalendarScreen extends StatefulWidget {
  const CalendarScreen({super.key});

  @override
  State<CalendarScreen> createState() => _CalendarScreenState();
}

class _CalendarScreenState extends State<CalendarScreen> {
  DateTime _focusedDay = DateTime.now();
  DateTime? _selectedDay;

  Map<DateTime, List<EmotionRecord>> emotionRecords = {};

  @override
  void initState() {
    super.initState();
    _loadMonthlyEmotions(_focusedDay);
  }

  Future<void> _loadMonthlyEmotions(DateTime month) async {
    try {
      final data = await EmotionService.fetchMonthlySummary(month);
      setState(() {
        emotionRecords = data;
      });
    } catch (e) {
      print('월별 감정 로딩 실패: $e');
    }
  }

  Future<void> _loadDailyEmotions(DateTime date) async {
    try {
      final records = await EmotionService.fetchDailyEmotions(date);

      if (records.isNotEmpty) {
        setState(() {
          emotionRecords[date] = records;
        });
        _showEmotionRecordViewer(date, records);
      } else {
        _showEmotionInputDialog(date);
      }
    } catch (e) {
      print('일별 감정 로딩 실패: $e');
      _showEmotionInputDialog(date);
    }
  }

  void _onDaySelected(DateTime selectedDay, DateTime focusedDay) {
    final dateOnly = DateTime(
      selectedDay.year,
      selectedDay.month,
      selectedDay.day,
    );
    setState(() {
      _selectedDay = dateOnly;
      _focusedDay = focusedDay;
    });
    _loadDailyEmotions(dateOnly);
  }

  void _showEmotionInputDialog(DateTime date, {int? existingIndex}) {
    final existingList = emotionRecords[date];
    final existingRecord =
        (existingIndex != null &&
                existingList != null &&
                existingIndex >= 0 &&
                existingIndex < existingList.length)
            ? existingList[existingIndex]
            : null;

    showDialog(
      context: context,
      barrierDismissible: false,
      barrierColor: Colors.black.withOpacity(0),
      builder: (context) {
        return Dialog(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
          ),
          child: EmotionInputDialog(
            date: date,
            existingRecord: existingRecord,
            onSave: (record) {
              setState(() {
                if (existingIndex != null) {
                  emotionRecords[date]![existingIndex] = record;
                } else {
                  emotionRecords[date] =
                      (emotionRecords[date] ?? [])..add(record);
                }
              });
              Navigator.pop(context);
            },
          ),
        );
      },
    );
  }

  void _showEmotionFromTextDialog(DateTime date) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder:
          (_) => EmotionFromTextDialog(
            onSubmit: (title, text) async {
              try {
                Navigator.pop(context);

                final record = await EmotionService.analyzeAndSave(
                  date: date,
                  title: title,
                  text: text,
                );

                setState(() {
                  emotionRecords[date] = [record];
                });

                _showEmotionRecordViewer(date, [record]);
              } catch (e) {
                print("❗ 감정 저장 실패 (onSubmit): ${e.toString()}");
                if (e is DioException) {
                  print('❗ DioException 응답: ${e.response}');
                  print('❗ DioException 메시지: ${e.message}');
                }
              }
            },
          ),
    );
  }

  void _showEmotionRecordViewer(DateTime date, List<EmotionRecord> records) {
    showDialog(
      context: context,
      builder:
          (context) => EmotionRecordViewerDialog(
            records: records,
            onEdit:
                (index) => _showEmotionInputDialog(date, existingIndex: index),
            onDelete: (index) async {
              final record = records[index];
              if (record.seq != null) {
                try {
                  await EmotionService.deleteEmotionRecord(record.seq!);
                } catch (e) {
                  print('서버 삭제 실패: $e');
                }
              }

              setState(() {
                emotionRecords[date]!.removeAt(index);
                if (emotionRecords[date]!.isEmpty) {
                  emotionRecords.remove(date);
                }
              });

              Navigator.pop(context);

              final updated = emotionRecords[date];
              if (updated != null && updated.isNotEmpty) {
                Future.delayed(const Duration(milliseconds: 100), () {
                  _showEmotionRecordViewer(date, updated);
                });
              }
            },
            onAdd: () {
              Navigator.pop(context);
              _showEmotionInputDialog(date);
            },
          ),
    );
  }

  Widget _buildEmotionForDay(DateTime day) {
    final records = emotionRecords[day];
    final first = records?.isNotEmpty == true ? records!.first : null;

    if (first == null) {
      return Image.asset('assets/emotions/none.png', width: 28, height: 28);
    }

    if (first.emotion.startsWith('http')) {
      return Image.network(first.emotion, width: 28, height: 28);
    }

    return Image.asset(
      'assets/emotions/${first.emotion}.png',
      width: 28,
      height: 28,
    );
  }

  Widget _buildDayCell(DateTime day, bool isSelected) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        const SizedBox(height: 6),
        isSelected
            ? Container(
              width: 30,
              height: 30,
              decoration: const BoxDecoration(
                color: Color(0xFF28B960),
                shape: BoxShape.circle,
              ),
              alignment: Alignment.center,
              child: Text(
                '${day.day}',
                style: const TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                ),
              ),
            )
            : Text('${day.day}', style: const TextStyle(fontSize: 16)),
        const SizedBox(height: 4),
        _buildEmotionForDay(day),
      ],
    );
  }

  void _moveMonth(int offset) {
    setState(() {
      _focusedDay = DateTime(_focusedDay.year, _focusedDay.month + offset);
    });
    _loadMonthlyEmotions(_focusedDay);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).scaffoldBackgroundColor,
      appBar: const CustomHeader(showBackButton: false),
      body: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const Text(
              "감정 캘린더",
              style: TextStyle(fontSize: 18, color: Colors.black87),
            ),
            const SizedBox(height: 24),
            Expanded(
              child: SingleChildScrollView(
                child: Column(
                  children: [
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 24),
                      child: Stack(
                        alignment: Alignment.center,
                        children: [
                          Align(
                            alignment: Alignment.centerLeft,
                            child: IconButton(
                              icon: const Icon(Icons.chevron_left),
                              onPressed: () => _moveMonth(-1),
                            ),
                          ),
                          Column(
                            children: [
                              Text(
                                '${_focusedDay.year}',
                                style: const TextStyle(fontSize: 18),
                              ),
                              Text(
                                '${_focusedDay.month}',
                                style: const TextStyle(
                                  fontSize: 28,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                          ),
                          Align(
                            alignment: Alignment.centerRight,
                            child: IconButton(
                              icon: const Icon(Icons.chevron_right),
                              onPressed: () => _moveMonth(1),
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 8),
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 16),
                      child: TableCalendar(
                        locale: 'ko_KR',
                        rowHeight: 90,
                        daysOfWeekHeight: 32,
                        firstDay: DateTime.utc(2020, 1, 1),
                        lastDay: DateTime.utc(2030, 12, 31),
                        focusedDay: _focusedDay,
                        headerVisible: false,
                        calendarFormat: CalendarFormat.month,
                        selectedDayPredicate:
                            (day) => isSameDay(day, _selectedDay),
                        onDaySelected: _onDaySelected,
                        daysOfWeekStyle: const DaysOfWeekStyle(
                          weekdayStyle: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                          weekendStyle: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        calendarStyle: const CalendarStyle(
                          outsideDaysVisible: false,
                        ),
                        calendarBuilders: CalendarBuilders(
                          defaultBuilder:
                              (context, day, _) => _buildDayCell(day, false),
                          todayBuilder:
                              (context, day, _) => _buildDayCell(day, false),
                          selectedBuilder:
                              (context, day, _) => _buildDayCell(day, true),
                        ),
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
    );
  }
}
