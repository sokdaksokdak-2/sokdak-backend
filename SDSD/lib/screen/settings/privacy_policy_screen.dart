import 'package:flutter/material.dart';
import 'package:sdsd/widgets/custom_header.dart';

class PrivacyPolicyScreen extends StatelessWidget {
  const PrivacyPolicyScreen({super.key});

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
                '개인정보 처리방침',
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
                        Text(
                          '속닥이(이하 "서비스")는 사용자의 소중한 개인정보를 보호하기 위해, 관련 법령을 준수하며 다음과 같은 정책에 따라 개인정보를 수집, 이용, 보관 및 파기합니다.\n',
                          style: TextStyle(fontSize: 16, height: 1.5),
                        ),

                        SectionTitle('1. 개인정보 수집 항목 및 수집 방법'),
                        BulletText(
                          '필수 수집 항목: 닉네임, 감정 기록(텍스트 또는 음성), 이용기록, 기기 정보(기종, OS 버전 등)',
                        ),
                        BulletText('선택 수집 항목: 캐릭터 이름, 회복 미션 설정 정보 등'),
                        BulletText(
                          '수집 방법: 앱 내 사용자 입력, 음성 인식, 자동 수집 기술(로그, 기기 정보 등)\n',
                        ),

                        SectionTitle('2. 개인정보 수집 및 이용 목적'),
                        BulletText('감정 기록 및 시각화(감정 캘린더, 리포트 제공 등)'),
                        BulletText('감정 기반 피드백 제공 및 캐릭터 반응 기능'),
                        BulletText('맞춤 회복 미션 제공'),
                        BulletText('사용자 문의 응대 및 앱 안정성 개선'),
                        BulletText('법령에 따른 보관 의무 준수를 위한 기록 관리\n'),

                        SectionTitle('3. 개인정보 보유 및 이용 기간'),
                        BulletText('서비스 이용 중 수집된 개인정보는 회원 탈퇴 시 즉시 파기됩니다.'),
                        BulletText(
                          '단, 관련 법령에 따라 일정 기간 보관이 필요한 정보는 예외적으로 해당 기간 동안 보관됩니다. (예: 전자상거래법, 통신비밀보호법 등)\n',
                        ),

                        SectionTitle('4. 개인정보 제3자 제공'),
                        BulletText('서비스는 사용자의 개인정보를 제3자에게 제공하지 않습니다.'),
                        BulletText('단, 법령에 근거하거나 수사기관의 요청이 있는 경우는 예외로 합니다.\n'),

                        SectionTitle('5. 개인정보 처리 위탁'),
                        BulletText(
                          '현재 서비스는 개인정보를 외부에 위탁하지 않으며, 향후 위탁이 발생할 경우 사용자에게 사전 고지하고 동의를 받습니다.\n',
                        ),

                        SectionTitle('6. 개인정보 파기 절차 및 방법'),
                        BulletText('회원 탈퇴 또는 수집 목적 달성 시 개인정보는 지체 없이 파기됩니다.'),
                        BulletText('전자적 파일 형태: 복구 불가능한 방식으로 삭제'),
                        BulletText('종이 문서 형태: 분쇄 또는 소각\n'),

                        SectionTitle('7. 이용자의 권리와 행사 방법'),
                        BulletText(
                          '이용자는 언제든지 자신의 감정 기록 및 정보를 열람, 수정, 삭제하거나 처리 정지를 요청할 수 있습니다.',
                        ),
                        BulletText('앱 내 ‘내 정보 관리’ 또는 고객 문의를 통해 요청할 수 있습니다.\n'),

                        SectionTitle('8. 개인정보 보호를 위한 노력'),
                        BulletText(
                          '서비스는 암호화, 접근 제한 등 기술적·관리적 보호 조치를 적용하고 있습니다.',
                        ),
                        BulletText(
                          '민감 정보에 대한 접근은 최소화되며, 내부 교육과 점검을 주기적으로 시행합니다.\n',
                        ),

                        SectionTitle('9. 개인정보 보호책임자 안내'),
                        BulletText('이름: 속닥이 운영팀'),
                        BulletText('이메일: support.sdsd@gmail.com\n'),

                        Text(
                          '당신의 감정은 소중합니다.\n속닥이는 그 마음을 지키기 위해 언제나 최선을 다할게요.',
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

// ✅ 줄바꿈 들여쓰기까지 예쁜 목록 항목 위젯
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
