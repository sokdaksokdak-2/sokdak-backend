import 'package:flutter/material.dart';

class EmotionFromTextDialog extends StatefulWidget {
  final Function(String title, String content) onSubmit;

  const EmotionFromTextDialog({super.key, required this.onSubmit});

  @override
  State<EmotionFromTextDialog> createState() => _EmotionFromTextDialogState();
}

class _EmotionFromTextDialogState extends State<EmotionFromTextDialog> {
  final _titleController = TextEditingController();
  final _textController = TextEditingController();

  bool isLoading = false;

  void _submit() {
    final title = _titleController.text.trim();
    final content = _textController.text.trim();

    if (title.isEmpty || content.isEmpty) return;

    setState(() => isLoading = true);

    widget.onSubmit(title, content);
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      insetPadding: const EdgeInsets.symmetric(horizontal: 24),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text(
              '오늘의 감정 생성하기',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _titleController,
              decoration: const InputDecoration(labelText: '제목'),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _textController,
              decoration: const InputDecoration(labelText: '내용 (텍스트 기반)'),
              maxLines: 4,
            ),
            const SizedBox(height: 20),
            isLoading
                ? const CircularProgressIndicator()
                : ElevatedButton(
                  onPressed: _submit,
                  child: const Text('감정 분석 시작'),
                ),
          ],
        ),
      ),
    );
  }
}
