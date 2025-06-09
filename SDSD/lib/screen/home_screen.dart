import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';
import 'package:sdsd/config.dart';
import 'package:sdsd/models/emotion_record.dart';
import 'package:sdsd/services/emotion_service.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:sdsd/widgets/custom_header.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late stt.SpeechToText _speech;
  bool isListening = false;
  bool isFirstMessage = true; // ✅ 최초 메시지 여부
  String spokenText = '';
  String serverResponse = '';

  Map<DateTime, List<EmotionRecord>> emotionRecords = {};

  @override
  void initState() {
    super.initState();
    _speech = stt.SpeechToText();
  }

  Future<void> _toggleListening() async {
    if (!isListening) {
      bool available = await _speech.initialize(
        onStatus: (status) => print('✅ STT 상태: $status'),
        onError: (error) => print('❌ STT 오류: $error'),
      );
      if (available) {
        setState(() {
          isListening = true;
          spokenText = '';
        });
        _speech.listen(
          localeId: 'ko_KR',
          onResult: (result) {
            setState(() {
              spokenText = result.recognizedWords;
            });
            print('🎤 인식된 텍스트: ${result.recognizedWords}');

            if (result.finalResult) {
              print('✅ 최종 인식 텍스트: ${result.recognizedWords}');
              sendTextToServer(result.recognizedWords);
            }
          },
        );
      }
    } else {
      setState(() => isListening = false);
      _speech.stop();
      print('🛑 음성 인식 중지');
    }
  }

  Future<void> sendTextToServer(String text) async {
    final uri = Uri.parse('${Config.baseUrl}/api/chatbot/stream');
    print('📤 서버로 보낼 텍스트: $text');

    try {
      final response = await http.post(
        uri,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: jsonEncode({
          'user_message': text,
          'member_seq': Config.memberSeq,
        }),
      );

      print('📥 응답 상태 코드: ${response.statusCode}');
      print('📥 응답 본문: ${response.body}');

      if (response.statusCode == 200) {
        setState(() {
          serverResponse =
              response.body.isNotEmpty ? response.body : '(응답은 200이지만 본문이 없음)';
          isFirstMessage = false;
        });

        // ✅ 감정 분석 및 저장
        final now = DateTime.now();
        final key = DateTime(now.year, now.month, now.day);

        final emotionRecord = await EmotionService.analyzeAndSave(
          date: now,
          text: text,
          title: '감정 분석 기록',
        );

        setState(() {
          if (emotionRecords.containsKey(key)) {
            emotionRecords[key]!.add(emotionRecord);
          } else {
            emotionRecords[key] = [emotionRecord];
          }
        });

        print('✅ 감정 기록 저장 완료: $emotionRecord');
      } else {
        setState(() {
          serverResponse = '서버 오류: ${response.statusCode}';
          isFirstMessage = false;
        });
      }
    } catch (e) {
      print("❗예외 발생: $e");
      setState(() {
        serverResponse = '지금은 통신 중이 아니에요...\n 속닥이가 다시 연결 중! ';
        isFirstMessage = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;

    return Scaffold(
      backgroundColor: Theme.of(context).scaffoldBackgroundColor,
      appBar: const CustomHeader(),
      body: SafeArea(
        child: Stack(
          children: [
            // 메인 콘텐츠
            Padding(
              padding: const EdgeInsets.only(top: 0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  const SizedBox(height: 60),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 60),
                    child: Container(
                      width: double.infinity,
                      padding: const EdgeInsets.symmetric(
                        vertical: 30,
                        horizontal: 20,
                      ),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(20),
                        boxShadow: const [
                          BoxShadow(
                            color: Colors.black12,
                            blurRadius: 6,
                            offset: Offset(0, 3),
                          ),
                        ],
                      ),
                      child: Text(
                        isFirstMessage
                            ? '안녕 ${Config.nickname.isNotEmpty ? Config.nickname : '속닥'}!\n오늘 하루는 어땠어??'
                            : serverResponse,
                        textAlign: TextAlign.center,
                        style: const TextStyle(fontSize: 20),
                      ),
                    ),
                  ),
                  const SizedBox(height: 8),

                  // 캐릭터 이미지
                  Expanded(
                    child: Center(
                      child: Image.asset(
                        'assets/images/happy.png',
                        height: 330,
                        fit: BoxFit.contain,
                      ),
                    ),
                  ),
                  const SizedBox(height: 140),
                ],
              ),
            ),

            // 🎤 Lottie 애니메이션
            if (isListening)
              Align(
                alignment: Alignment.bottomCenter,
                child: Padding(
                  padding: const EdgeInsets.only(bottom: 20),
                  child: SizedBox(
                    width: 120,
                    height: 120,
                    child: Lottie.asset(
                      'assets/lottie/mic.json',
                      repeat: true,
                      animate: true,
                    ),
                  ),
                ),
              ),

            // 🎤 마이크 버튼
            Align(
              alignment: Alignment.bottomCenter,
              child: Padding(
                padding: const EdgeInsets.only(bottom: 50),
                child: GestureDetector(
                  onTap: _toggleListening,
                  child: AnimatedContainer(
                    duration: const Duration(milliseconds: 150),
                    width: 60,
                    height: 60,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      gradient:
                          isListening
                              ? const LinearGradient(
                                colors: [Color(0xFFBDBDBD), Color(0xFF8E8E8E)],
                                begin: Alignment.topLeft,
                                end: Alignment.bottomRight,
                              )
                              : const LinearGradient(
                                colors: [Color(0xFFDADADA), Color(0xFFAAAAAA)],
                                begin: Alignment.topLeft,
                                end: Alignment.bottomRight,
                              ),
                      boxShadow:
                          isListening
                              ? [
                                const BoxShadow(
                                  color: Colors.white,
                                  offset: Offset(-2, -2),
                                  blurRadius: 2,
                                ),
                                const BoxShadow(
                                  color: Colors.black26,
                                  offset: Offset(2, 2),
                                  blurRadius: 2,
                                ),
                              ]
                              : [
                                const BoxShadow(
                                  color: Colors.black26,
                                  offset: Offset(4, 4),
                                  blurRadius: 8,
                                ),
                                const BoxShadow(
                                  color: Colors.white,
                                  offset: Offset(-4, -4),
                                  blurRadius: 8,
                                ),
                              ],
                    ),
                    child: const Center(
                      child: Icon(Icons.mic, size: 45, color: Colors.black),
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
