import 'package:flutter/material.dart';

class CustomHeader extends StatelessWidget implements PreferredSizeWidget {
  final bool showBackButton;
  final Widget? rightWidget;
  final String? subtitle;

  const CustomHeader({
    this.showBackButton = false,
    this.rightWidget,
    this.subtitle,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Container(
        color: Theme.of(context).scaffoldBackgroundColor,
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        child: Stack(
          alignment: Alignment.center,
          children: [
            // 좌측 공간 확보
            Align(
              alignment: Alignment.centerLeft,
              child:
                  showBackButton
                      ? IconButton(
                        icon: const Icon(Icons.arrow_back),
                        onPressed: () => Navigator.pop(context),
                      )
                      : const SizedBox(width: 48), // ← 버튼 없을 때도 공간 유지
            ),
            Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const SizedBox(height: 16),
                Image.asset("assets/images/sdsd1.png", height: 40),
                if (subtitle != null)
                  Padding(
                    padding: const EdgeInsets.only(top: 4, bottom: 4),
                    child: Text(
                      subtitle!,
                      style: const TextStyle(fontSize: 14, color: Colors.black),
                    ),
                  ),
              ],
            ),
            if (rightWidget != null)
              Align(alignment: Alignment.centerRight, child: rightWidget),
          ],
        ),
      ),
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(80);
}
