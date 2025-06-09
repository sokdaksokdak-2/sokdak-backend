import 'package:flutter/material.dart';
import 'package:siri_wave/siri_wave.dart';

void main() {
  runApp(const MaterialApp(home: WaveTest()));
}

class WaveTest extends StatelessWidget {
  const WaveTest({super.key});

  @override
  Widget build(BuildContext context) {
    final controller = IOS9SiriWaveformController(
      amplitude: 0.5,
      color1: Colors.red,
      color2: Colors.green,
      color3: Colors.blue,
      speed: 0.15,
    );

    return Scaffold(
      backgroundColor: Colors.grey[200],
      body: Center(
        child: Stack(
          alignment: Alignment.center,
          children: [
            // Siri 파형
            SizedBox(
              width: 400,
              height: 600,
              child: SiriWaveform.ios9(
                controller: controller,
                options: const IOS9SiriWaveformOptions(
                  width: 400,
                  height: 600,
                ),
              ),
            ),

            // 가운데 동그라미 아이콘
            Container(
              width: 80,
              height: 80,
              decoration: const BoxDecoration(
                color: Colors.grey,
                shape: BoxShape.circle,
              ),
              child: const Icon(Icons.mic, color: Colors.black, size: 40),
            ),
          ],
        ),
      ),
    );
  }
}
