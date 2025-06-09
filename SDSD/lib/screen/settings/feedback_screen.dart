import 'package:flutter/material.dart';
import 'package:sdsd/widgets/custom_header.dart';

class FeedbackScreen extends StatefulWidget {
  const FeedbackScreen({super.key});

  @override
  State<FeedbackScreen> createState() => _FeedbackScreenState();
}

class _FeedbackScreenState extends State<FeedbackScreen> {
  final TextEditingController _controller = TextEditingController();

  void _submitFeedback() {
    final text = _controller.text.trim();
    if (text.isNotEmpty) {
      // 실제 전송 로직을 여기에 추가
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          behavior: SnackBarBehavior.floating,
          backgroundColor: Colors.grey[500],
          elevation: 6,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          margin: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
          duration: const Duration(seconds: 2),
          content: Row(
            children: [
              CircleAvatar(
                radius: 12,
                backgroundColor: const Color(0xFF28B960), // 초록 원
                child: const Icon(
                  Icons.check,
                  size: 20,
                  color: Colors.white, // 흰색 체크!
                ),
              ),
              const SizedBox(width: 12),
              const Expanded(
                child: Text(
                  '소중한 의견 감사합니다!',
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
      _controller.clear();
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
                '의견 보내기',
                style: TextStyle(fontSize: 18, color: Colors.black87),
              ),
              const SizedBox(height: 34),
              Expanded(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.symmetric(horizontal: 24),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      Center(
                        child: Container(
                          // ✅ 크기 조절: 너비/높이 직접 조절 가능
                          width: 330,
                          // ← 원하는 너비 (예: 320)
                          constraints: const BoxConstraints(
                            minHeight: 380, // ← 최소 높이
                            // maxHeight: 600, // ← 최대 높이 (제한 없애려면 제거해도 됨)
                          ),
                          padding: const EdgeInsets.symmetric(
                            horizontal: 28, // ← 내부 좌우 여백
                            vertical: 28, // ↑↓ 내부 상하 여백
                          ),
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(16),
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text(
                                '피드백을 들려주세요.',
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 20,
                                ),
                              ),
                              const SizedBox(height: 10),
                              const Text(
                                '속닥속닥을 더 따뜻하게 만들기 위한\n여러분의 소중한 의견을 기다려요.',
                                style: TextStyle(
                                  fontSize: 16,
                                  color: Colors.black87,
                                ),
                              ),
                              const SizedBox(height: 24),
                              TextField(
                                controller: _controller,
                                maxLines: 6,
                                decoration: InputDecoration(
                                  hintText: '불편했던 점이나 개선 아이디어를 자유롭게 적어주세요.',
                                  hintStyle: const TextStyle(
                                    fontSize: 15,
                                    color: Colors.grey,
                                  ),
                                  contentPadding: const EdgeInsets.symmetric(
                                    horizontal: 22,
                                    vertical: 22,
                                  ),
                                  enabledBorder: OutlineInputBorder(
                                    borderSide: BorderSide(
                                      color: Colors.grey.shade300,
                                    ),
                                    borderRadius: BorderRadius.circular(10),
                                  ),
                                  focusedBorder: OutlineInputBorder(
                                    borderSide: BorderSide(
                                      color: Colors.grey.shade400,
                                    ),
                                    borderRadius: BorderRadius.circular(10),
                                  ),
                                ),
                              ),
                              const SizedBox(height: 24),
                              Center(
                                child: SizedBox(
                                  width: 150,
                                  height: 36, // ← 버튼 높이
                                  child: ElevatedButton(
                                    style: ElevatedButton.styleFrom(
                                      backgroundColor: const Color(0xFF28B960),
                                      shape: RoundedRectangleBorder(
                                        borderRadius: BorderRadius.circular(6),
                                      ),
                                      padding: const EdgeInsets.symmetric(
                                        horizontal: 20,
                                      ),
                                    ),
                                    onPressed: _submitFeedback,
                                    child: const Text(
                                      '보내기',
                                      style: TextStyle(
                                        color: Colors.white,
                                        fontSize: 15,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                            ],
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
      ),
    );
  }
}
