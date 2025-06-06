import 'package:flutter/material.dart';
import 'package:sdsd/widgets/custom_header.dart';

class TermsOfServiceScreen extends StatelessWidget {
  const TermsOfServiceScreen({super.key});

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
                '서비스 이용약관',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.black87,
                ),
              ),
              const SizedBox(height: 24),
              Container(
                margin: const EdgeInsets.symmetric(horizontal: 24),
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(16),
                ),
                height: 600,
                child: Scrollbar(
                  thumbVisibility: true,
                  child: SingleChildScrollView(
                    child: const Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        SectionTitle('1. 약관의 목적'),
                        Text(
                          '이 약관은 ‘속닥이(이하 "서비스")’가 제공하는 모든 서비스 이용과 관련하여 회사와 이용자 간의 권리, 의무 및 책임사항을 규정함을 목적으로 합니다.\n',
                          style: TextStyle(fontSize: 16, height: 1.5),
                        ),

                        SectionTitle('2. 용어의 정의'),
                        BulletText(
                          '“서비스”란 사용자의 감정 인식 및 기록, 캐릭터 대화, 회복 미션 등의 기능을 제공하는 애플리케이션을 의미합니다.',
                        ),
                        BulletText(
                          '“이용자”란 본 약관에 따라 서비스를 이용하는 모든 사용자(회원 및 비회원 포함)를 말합니다.',
                        ),
                        BulletText(
                          '“회원”이란 서비스에 닉네임을 등록하고, 감정 기록 등 개인화 기능을 이용하는 사용자를 말합니다.\n',
                        ),

                        SectionTitle('3. 서비스의 제공 및 변경'),
                        BulletText(
                          '회사는 감정 기록, 리포트, 캐릭터 대화, 회복 미션 등 다양한 감정 기반 기능을 제공합니다.',
                        ),
                        BulletText(
                          '필요 시 서비스 내용은 변경될 수 있으며, 사전 공지를 통해 안내됩니다.\n',
                        ),

                        SectionTitle('4. 이용자의 권리와 의무'),
                        BulletText(
                          '이용자는 서비스를 자유롭게 사용할 수 있으며, 기록된 감정 데이터에 대한 열람 및 삭제 권한을 가집니다.',
                        ),
                        BulletText(
                          '이용자는 타인의 개인정보를 침해하거나, 비정상적인 방식으로 서비스를 악용해서는 안 됩니다.\n',
                        ),

                        SectionTitle('5. 개인정보 보호'),
                        BulletText(
                          '서비스는 사용자의 감정 기록, 닉네임 등 민감한 정보를 안전하게 보호합니다.',
                        ),
                        BulletText(
                          '개인정보는 이용자의 동의 없이 제3자에게 제공되지 않으며, 관련 법령에 따라 보호됩니다.',
                        ),
                        BulletText('자세한 내용은 ‘개인정보 처리방침’을 따릅니다.\n'),

                        SectionTitle('6. 서비스 이용의 제한 및 해지'),
                        BulletText('이용자가 다음과 같은 행위를 하는 경우 서비스 이용이 제한될 수 있습니다:'),
                        BulletText('① 타인의 정보를 도용한 경우'),
                        BulletText('② 욕설, 혐오, 폭력 등의 언어를 입력한 경우'),
                        BulletText('③ 시스템을 악의적으로 해킹하거나 오류를 유발하는 경우'),
                        BulletText(
                          '사용자는 언제든지 회원 탈퇴를 요청할 수 있으며, 탈퇴 시 모든 감정 기록은 즉시 삭제됩니다.\n',
                        ),

                        SectionTitle('7. 책임의 제한'),
                        Text(
                          '서비스는 감정 위로와 기록을 위한 도구이며, 전문적인 의료 또는 심리 상담을 대체하지 않습니다.\n',
                          style: TextStyle(fontSize: 16, height: 1.5),
                        ),

                        SectionTitle('8. 기타'),
                        Text(
                          '본 약관은 관련 법령에 위배되지 않는 범위에서 개정될 수 있으며, 변경 시 사전 공지를 통해 안내합니다.\n',
                          style: TextStyle(fontSize: 16, height: 1.5),
                        ),

                        Text(
                          '당신의 감정을 소중히 다루기 위해, 이 약속을 함께 지켜나갈게요.\n궁금한 점이나 불편한 부분이 있다면 언제든 속닥이에게 이야기해 주세요.',
                          style: TextStyle(fontSize: 16, height: 1.5),
                        ),
                      ],
                    ),
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

// ✅ 대제목 위젯
class SectionTitle extends StatelessWidget {
  final String text;

  const SectionTitle(this.text, {super.key});

  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      style: const TextStyle(
        fontWeight: FontWeight.bold,
        fontSize: 16,
        height: 2,
      ),
    );
  }
}

// ✅ 줄바꿈 들여쓰기 정리된 항목 위젯
class BulletText extends StatelessWidget {
  final String text;

  const BulletText(this.text, {super.key});

  @override
  Widget build(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('・ ', style: TextStyle(fontSize: 16, height: 1.5)),
        Expanded(
          child: Text(text, style: const TextStyle(fontSize: 16, height: 1.5)),
        ),
      ],
    );
  }
}
