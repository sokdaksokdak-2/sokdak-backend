import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:sdsd/config.dart';
import 'package:sdsd/services/emotion_service.dart';
import '../models/emotion_record.dart';

class EmotionInputDialog extends StatefulWidget {
  final DateTime date;
  final EmotionRecord? existingRecord;
  final void Function(EmotionRecord) onSave;

  const EmotionInputDialog({
    super.key,
    required this.date,
    required this.onSave,
    this.existingRecord,
  });

  @override
  State<EmotionInputDialog> createState() => _EmotionInputDialogState();
}

class _EmotionInputDialogState extends State<EmotionInputDialog> {
  String? selectedEmotion;
  late TextEditingController titleController;
  late TextEditingController contentController;

  final Map<String, int> emotionMap = {
    'cropped_happy': 1,
    'cropped_fear': 2,
    'cropped_angry': 3,
    'cropped_sad': 4,
    'cropped_soso': 5,
  };

  @override
  void initState() {
    super.initState();
    selectedEmotion = widget.existingRecord?.emotion;
    titleController = TextEditingController(
      text: widget.existingRecord?.title ?? '',
    );
    contentController = TextEditingController(
      text: widget.existingRecord?.content ?? '',
    );
  }

  @override
  void dispose() {
    titleController.dispose();
    contentController.dispose();
    super.dispose();
  }

  String _emotionLabel(String emotion) {
    switch (emotion) {
      case 'cropped_happy':
        return '행복';
      case 'cropped_fear':
        return '불안';
      case 'cropped_angry':
        return '분노';
      case 'cropped_sad':
        return '슬픔';
      case 'cropped_soso':
        return '평온';
      default:
        return '';
    }
  }

  @override
  Widget build(BuildContext context) {
    final emotions = [
      'cropped_happy',
      'cropped_fear',
      'cropped_angry',
      'cropped_sad',
      'cropped_soso',
    ];

    return Container(
      constraints: const BoxConstraints(minHeight: 550, maxWidth: 325),
      decoration: BoxDecoration(
        color: Colors.grey[100],
        borderRadius: BorderRadius.circular(20),
      ),
      padding: const EdgeInsets.all(20),
      child: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const SizedBox(height: 22),
            const Padding(
              padding: EdgeInsets.only(left: 8),
              child: Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  "기분 어때?",
                  style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
                ),
              ),
            ),
            const SizedBox(height: 8),
            Container(
              padding: const EdgeInsets.symmetric(vertical: 10),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(12),
              ),
              child: SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children:
                      emotions.map((emotion) {
                        final isSelected = selectedEmotion == emotion;
                        return GestureDetector(
                          onTap:
                              () => setState(() => selectedEmotion = emotion),
                          child: Padding(
                            padding: const EdgeInsets.symmetric(horizontal: 8),
                            child: Opacity(
                              opacity: isSelected ? 1.0 : 0.3,
                              child: Column(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  Image.asset(
                                    'assets/emotions/$emotion.png',
                                    width: 36,
                                  ),
                                  const SizedBox(height: 4),
                                  Text(
                                    _emotionLabel(emotion),
                                    style: TextStyle(
                                      fontSize: 12,
                                      fontWeight:
                                          isSelected
                                              ? FontWeight.bold
                                              : FontWeight.normal,
                                      color: Colors.black,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ),
                        );
                      }).toList(),
                ),
              ),
            ),

            const SizedBox(height: 25),

            const Padding(
              padding: EdgeInsets.only(left: 8),
              child: Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  "제목",
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                ),
              ),
            ),
            const SizedBox(height: 8),
            TextField(
              controller: titleController,
              style: const TextStyle(fontSize: 14),
              decoration: InputDecoration(
                filled: true,
                fillColor: Colors.white,
                contentPadding: const EdgeInsets.symmetric(
                  horizontal: 12,
                  vertical: 14,
                ),
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide.none,
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(color: Colors.green),
                ),
              ),
            ),

            const SizedBox(height: 25),

            const Padding(
              padding: EdgeInsets.only(left: 8),
              child: Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  "내용",
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                ),
              ),
            ),
            const SizedBox(height: 8),
            TextField(
              controller: contentController,
              maxLines: 6,
              style: const TextStyle(fontSize: 14),
              decoration: InputDecoration(
                filled: true,
                fillColor: Colors.white,
                contentPadding: const EdgeInsets.symmetric(
                  horizontal: 12,
                  vertical: 14,
                ),
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide.none,
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(color: Colors.green),
                ),
              ),
            ),

            const SizedBox(height: 20),

            Row(
              children: [
                Expanded(
                  child: ElevatedButton(
                    onPressed: () => Navigator.pop(context),
                    style: ElevatedButton.styleFrom(
                      minimumSize: Size.zero,
                      backgroundColor: Colors.white,
                      foregroundColor: Colors.black,
                      padding: const EdgeInsets.symmetric(vertical: 8),
                      elevation: 0,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                        side: const BorderSide(color: Colors.black12),
                      ),
                    ),
                    child: const Text('취소', style: TextStyle(fontSize: 14)),
                  ),
                ),
                const SizedBox(width: 20),
                Expanded(
                  child: ElevatedButton(
                    onPressed: () async {
                      final title = titleController.text.trim();
                      final content = contentController.text.trim();

                      if (selectedEmotion == null ||
                          title.isEmpty ||
                          content.isEmpty)
                        return;

                      final emotionSeq = emotionMap[selectedEmotion];
                      final formattedDate = DateFormat(
                        'yyyy-MM-dd',
                      ).format(widget.date);

                      try {
                        final record = EmotionRecord(
                          seq: widget.existingRecord?.seq,
                          emotion: selectedEmotion!,
                          title: title,
                          content: content,
                        );

                        await EmotionService.createEmotionManually(
                          memberSeq: Config.memberSeq,
                          // TODO: Replace with actual user ID
                          calendarDate: formattedDate,
                          title: title,
                          context: content,
                          emotionSeq: emotionSeq!,
                        );

                        widget.onSave(record);
                        Navigator.pop(context);
                      } catch (e) {
                        print('감정 저장 실패: ${e.toString()}');
                      }
                    },
                    style: ElevatedButton.styleFrom(
                      minimumSize: Size.zero,
                      backgroundColor: Colors.green,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 8),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    child: const Text('저장', style: TextStyle(fontSize: 14)),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
