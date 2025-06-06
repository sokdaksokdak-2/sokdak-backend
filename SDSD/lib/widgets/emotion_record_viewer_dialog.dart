import 'package:flutter/material.dart';
import '../models/emotion_record.dart';

class EmotionRecordViewerDialog extends StatelessWidget {
  final List<EmotionRecord> records;
  final void Function(int index) onEdit;
  final void Function(int index) onDelete;
  final VoidCallback onAdd;

  const EmotionRecordViewerDialog({
    super.key,
    required this.records,
    required this.onEdit,
    required this.onDelete,
    required this.onAdd,
  });

  @override
  Widget build(BuildContext context) {
    return Dialog(
      backgroundColor: Colors.grey[200],
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      insetPadding: const EdgeInsets.all(24),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 20),
        constraints: const BoxConstraints(maxHeight: 550, maxWidth: 325),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('감정 기록', style: TextStyle(fontSize: 18)),
            const SizedBox(height: 16),

            // 스크롤 영역 (둥근 테두리 유지)
            Expanded(
              child: ClipRRect(
                borderRadius: BorderRadius.circular(16),
                child: Scrollbar(
                  thumbVisibility: true,
                  thickness: 4,
                  radius: const Radius.circular(8),
                  child: SingleChildScrollView(
                    child: Container(
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(
                          color: Color(0xFFDADADA), // 💡 원하는 테두리 색상
                          width: 1, // 💡 테두리 두께
                        ),
                      ),
                      padding: const EdgeInsets.all(12),
                      child: Column(
                        children: List.generate(records.length * 2 - 1, (i) {
                          if (i.isEven) {
                            final index = i ~/ 2;
                            final record = records[index];
                            return Padding(
                              padding: const EdgeInsets.symmetric(
                                vertical: 8.0,
                              ),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    children: [
                                      Image.asset(
                                        'assets/emotions/${record.emotion}.png',
                                        width: 32,
                                        height: 32,
                                      ),
                                      const SizedBox(width: 8),
                                      Expanded(
                                        child: Text(
                                          record.title,
                                          style: const TextStyle(
                                            color: Color(0xFF4E4E4E),
                                            fontSize: 16,
                                            fontWeight: FontWeight.bold,
                                          ),
                                        ),
                                      ),
                                    ],
                                  ),
                                  const SizedBox(height: 6),
                                  Text(
                                    record.content,
                                    style: const TextStyle(fontSize: 14),
                                  ),
                                  const SizedBox(height: 6),
                                  Row(
                                    mainAxisAlignment: MainAxisAlignment.end,
                                    children: [
                                      ElevatedButton(
                                        onPressed: () => onDelete(index),
                                        style: ElevatedButton.styleFrom(
                                          minimumSize: Size.zero,
                                          backgroundColor: Colors.grey[200],
                                          foregroundColor: Colors.grey[800],
                                          // ✅ 텍스트 색상
                                          textStyle: const TextStyle(
                                            // ✅ 텍스트 스타일
                                            fontSize: 14,
                                            fontWeight: FontWeight.w600,
                                          ),
                                          shape: RoundedRectangleBorder(
                                            borderRadius: BorderRadius.circular(
                                              8,
                                            ),
                                          ),
                                          padding: const EdgeInsets.symmetric(
                                            horizontal: 10,
                                            vertical: 8,
                                          ),
                                        ),
                                        child: const Text('삭제'),
                                      ),
                                      const SizedBox(width: 8),
                                      ElevatedButton(
                                        onPressed: () => onEdit(index),
                                        style: ElevatedButton.styleFrom(
                                          minimumSize: Size.zero,
                                          backgroundColor: Color(0xFF28B960),
                                          foregroundColor: Colors.white,
                                          // ✅ 텍스트 색상
                                          textStyle: const TextStyle(
                                            // ✅ 텍스트 스타일
                                            fontSize: 14,
                                            fontWeight: FontWeight.w600,
                                          ),
                                          shape: RoundedRectangleBorder(
                                            borderRadius: BorderRadius.circular(
                                              8,
                                            ),
                                          ),
                                          padding: const EdgeInsets.symmetric(
                                            horizontal: 10,
                                            vertical: 8,
                                          ),
                                        ),
                                        child: const Text('수정'),
                                      ),
                                    ],
                                  ),
                                ],
                              ),
                            );
                          } else {
                            return const Divider(
                              color: Color(0xFFE5E0E0),
                              thickness: 0.5,
                              height: 24,
                            );
                          }
                        }),
                      ),
                    ),
                  ),
                ),
              ),
            ),

            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                // 왼쪽: 출력 + 공유
                Row(
                  children: [
                    // 출력 버튼
                    ElevatedButton(
                      onPressed: () {
                        // 출력 동작
                      },
                      style: ElevatedButton.styleFrom(
                        minimumSize: Size.zero,
                        backgroundColor: Colors.grey[300],
                        elevation: 0,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 2),
                        foregroundColor: Colors.black87,
                        textStyle: const TextStyle(fontSize: 12),
                      ),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: const [
                          Icon(Icons.file_download_outlined, size: 20),
                          // SizedBox(height: 0),
                          Text('출력'),
                        ],
                      ),
                    ),
                    const SizedBox(width: 10),

                    // 공유 버튼
                    ElevatedButton(
                      onPressed: () {
                        // 공유 동작
                      },
                      style: ElevatedButton.styleFrom(
                        minimumSize: Size.zero,
                        backgroundColor: Colors.grey[300],
                        elevation: 0,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 2),
                        foregroundColor: Colors.black87,
                        textStyle: const TextStyle(fontSize: 12),
                      ),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: const [
                          Icon(Icons.share_outlined, size: 20),
                          // SizedBox(height: 4),
                          Text('공유'),
                        ],
                      ),
                    ),
                  ],
                ),

                // 오른쪽: 닫기 + 추가 버튼
                Row(
                  children: [
                    ElevatedButton(
                      onPressed: () {
                        Navigator.pop(context); // ✅ 닫기 동작
                      },
                      style: ElevatedButton.styleFrom(
                        minimumSize: Size.zero,
                        backgroundColor: Colors.grey[500],
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                        padding: const EdgeInsets.symmetric(horizontal: 22, vertical: 8),
                        textStyle: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
                      ),
                      child: const Text('닫기'),
                    ),
                    const SizedBox(width: 8),
                    ElevatedButton(
                      onPressed: onAdd,
                      style: ElevatedButton.styleFrom(
                        minimumSize: Size.zero,
                        backgroundColor: Colors.black,
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                        padding: const EdgeInsets.symmetric(horizontal: 22, vertical: 8),
                        textStyle: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
                      ),
                      child: const Text('추가'),
                    ),
                  ],
                )
              ],
            ),

          ],
        ),
      ),
    );
  }
}
