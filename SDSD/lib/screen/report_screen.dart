import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../config.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../widgets/custom_header.dart';

class ReportScreen extends StatefulWidget {
  const ReportScreen({super.key});

  @override
  State<ReportScreen> createState() => _ReportScreenState();
}

class _ReportScreenState extends State<ReportScreen> {
  bool isLoading = true;
  bool hasError = false;
  bool noReport = false;
  Map<String, dynamic> emotionData = {};
  String summaryText = '';

  @override
  void initState() {
    super.initState();
    fetchEmotionReport();
  }

  Future<void> fetchEmotionReport() async {
    final now = DateTime.now();
    final year = now.year;
    final month = now.month;

    final uri = Uri.parse(
      '${Config.baseUrl}/api/emo_report/?year=$year&month=$month&member_seq=${Config.memberSeq}',
    );

    try {
      final response = await http.get(
        uri,
        headers: {'Authorization': 'Bearer ${Config.accessToken}'},
      );

      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body);
        setState(() {
          emotionData = Map<String, dynamic>.from(
            jsonData['emotion_distribution'],
          );
          summaryText = jsonData['summary_text'];
          isLoading = false;
        });
      } else if (response.statusCode == 404) {
        setState(() {
          noReport = true;
          isLoading = false;
        });
      } else {
        setState(() {
          hasError = true;
          isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        hasError = true;
        isLoading = false;
      });
    }
  }

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
                "월간 리포트",
                style: TextStyle(fontSize: 18, color: Colors.black87),
              ),
              const SizedBox(height: 34),
              Expanded(
                child:
                    isLoading
                        ? const Center(child: CircularProgressIndicator())
                        : hasError
                        ? const Center(child: Text('리포트를 불러올 수 없습니다.'))
                        : noReport
                        ? _buildEmptyState()
                        : SingleChildScrollView(
                          padding: const EdgeInsets.symmetric(horizontal: 20),
                          child: Column(
                            children: [
                              _buildEmotionChartCard(),
                              const SizedBox(height: 16),
                              _buildEmotionDiaryCard(),
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

  Widget _buildEmptyState() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.only(top: 0, left: 24, right: 24, bottom: 36),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Image.asset(
              'assets/images/sad.png',
              width: 300,
              height: 300,
            ),
            const SizedBox(height: 24),
            const Text(
              '이번 달 감정 리포트가 아직 없어요',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            const Text(
              '홈에서 마이크를 눌러 감정을 기록하면\n속닥이가 리포트를 만들어줄게요!',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 16, height: 1.5),
            ),
          ],
        ),
      ),
    );
  }


  Widget _buildEmotionChartCard() {
    final colorMap = {
      'angry': const Color(0xAAFFAFA3),
      'fear': const Color(0x88FFB356),
      'soso': const Color(0xAAFFED66),
      'happy': const Color(0xAA85E0A3),
      'sad': const Color(0xAA80CAFF),
    };

    final imageMap = {
      'angry': 'assets/emotions/cropped_angry.png',
      'fear': 'assets/emotions/cropped_fear.png',
      'soso': 'assets/emotions/cropped_soso.png',
      'happy': 'assets/emotions/cropped_happy.png',
      'sad': 'assets/emotions/cropped_sad.png',
    };

    final total = emotionData.values.fold<double>(
      0,
      (sum, e) => sum + (e as num).toDouble(),
    );
    final normalized = total.clamp(0, 100) / 100.0;

    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
      ),
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Text(
                '지난달 종합 감정지수',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const Spacer(),
              Text(
                '${(normalized * 100).toInt()}%',
                style: const TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          ClipRRect(
            borderRadius: BorderRadius.circular(10),
            child: LinearProgressIndicator(
              value: normalized,
              backgroundColor: Colors.grey[300],
              color: Colors.green,
              minHeight: 8,
            ),
          ),
          const SizedBox(height: 16),
          Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Expanded(
                child: SizedBox(
                  height: 200,
                  child: PieChart(
                    PieChartData(
                      startDegreeOffset: -120,
                      sectionsSpace: 0,
                      centerSpaceRadius: 45,
                      sections:
                          emotionData.entries.map((entry) {
                            final value = (entry.value as num).toDouble();
                            return PieChartSectionData(
                              value: value,
                              color: colorMap[entry.key],
                              radius: 50,
                              title: '${value.toInt()}%',
                              titleStyle: const TextStyle(
                                fontSize: 16,
                                color: Colors.black,
                              ),
                              titlePositionPercentageOffset: 0.6,
                            );
                          }).toList(),
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 16),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children:
                    emotionData.entries.map((entry) {
                      return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 6),
                        child: Row(
                          children: [
                            Container(
                              width: 12,
                              height: 12,
                              decoration: BoxDecoration(
                                color: colorMap[entry.key],
                                borderRadius: BorderRadius.circular(4),
                              ),
                            ),
                            const SizedBox(width: 8),
                            Text(
                              entry.key,
                              style: const TextStyle(
                                fontSize: 15,
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                            const SizedBox(width: 8),
                            Image.asset(
                              imageMap[entry.key] ?? '',
                              width: 28,
                              height: 28,
                            ),
                          ],
                        ),
                      );
                    }).toList(),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildEmotionDiaryCard() {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
      ),
      child: Text(
        summaryText,
        style: const TextStyle(fontSize: 16, height: 1.5),
      ),
    );
  }
}
