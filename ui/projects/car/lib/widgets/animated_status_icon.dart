import 'package:flutter/material.dart';
import 'dart:math' as math;

class AnimatedStatusIcon extends StatelessWidget {
  final String type;
  final double value;
  final double maxValue;
  final Color color;

  const AnimatedStatusIcon({
    Key? key,
    required this.type,
    required this.value,
    required this.maxValue,
    required this.color,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(8),
      ),
      child: SizedBox(
        width: 32,
        height: 32,
        child: CustomPaint(
          painter: _StatusIconPainter(
            type: type,
            progress: value / maxValue,
            color: color,
          ),
        ),
      ),
    );
  }
}

class _StatusIconPainter extends CustomPainter {
  final String type;
  final double progress;
  final Color color;

  _StatusIconPainter({
    required this.type,
    required this.progress,
    required this.color,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..strokeWidth = 2.0
      ..style = PaintingStyle.stroke;

    final fillPaint = Paint()
      ..color = color
      ..style = PaintingStyle.fill;

    switch (type) {
      case 'speed':
        _drawSpeedometer(canvas, size, paint, fillPaint);
        break;
      case 'fuel':
        _drawFuelPump(canvas, size, paint, fillPaint);
        break;
      case 'battery':
        _drawBattery(canvas, size, paint, fillPaint);
        break;
      case 'temperature':
        _drawThermometer(canvas, size, paint, fillPaint);
        break;
    }
  }

  void _drawSpeedometer(Canvas canvas, Size size, Paint paint, Paint fillPaint) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width / 2 - 2;

    // Draw background circle
    canvas.drawCircle(center, radius, paint);

    // Draw progress arc
    final rect = Rect.fromCircle(center: center, radius: radius);
    canvas.drawArc(
      rect,
      -math.pi * 0.75,
      math.pi * 1.5 * progress,
      false,
      paint..strokeWidth = 3,
    );

    // Draw needle
    final needleLength = radius - 4;
    final angle = -math.pi * 0.75 + (math.pi * 1.5 * progress);
    final needleEnd = Offset(
      center.dx + needleLength * math.cos(angle),
      center.dy + needleLength * math.sin(angle),
    );
    canvas.drawLine(center, needleEnd, fillPaint..strokeWidth = 2);
  }

  void _drawFuelPump(Canvas canvas, Size size, Paint paint, Paint fillPaint) {
    final rect = Rect.fromLTWH(4, 4, size.width - 8, size.height - 8);
    
    // Draw pump outline
    final pumpPath = Path()
      ..moveTo(rect.left, rect.bottom)
      ..lineTo(rect.left, rect.top + rect.height * 0.3)
      ..quadraticBezierTo(
        rect.left,
        rect.top,
        rect.left + rect.width * 0.3,
        rect.top,
      )
      ..lineTo(rect.right - rect.width * 0.3, rect.top)
      ..quadraticBezierTo(
        rect.right,
        rect.top,
        rect.right,
        rect.top + rect.height * 0.3,
      )
      ..lineTo(rect.right, rect.bottom)
      ..close();

    canvas.drawPath(pumpPath, paint);

    // Draw fill level
    final fillHeight = rect.height * progress;
    final fillRect = Rect.fromLTWH(
      rect.left + 2,
      rect.bottom - fillHeight,
      rect.width - 4,
      fillHeight,
    );
    canvas.drawRect(fillRect, fillPaint);
  }

  void _drawBattery(Canvas canvas, Size size, Paint paint, Paint fillPaint) {
    final rect = Rect.fromLTWH(2, 6, size.width - 6, size.height - 12);
    
    // Draw battery outline
    canvas.drawRRect(
      RRect.fromRectAndRadius(rect, const Radius.circular(2)),
      paint,
    );

    // Draw battery tip
    final tipRect = Rect.fromLTWH(
      rect.right,
      rect.top + rect.height * 0.25,
      4,
      rect.height * 0.5,
    );
    canvas.drawRect(tipRect, paint);

    // Draw fill level
    if (progress > 0) {
      final fillRect = Rect.fromLTWH(
        rect.left + 2,
        rect.top + 2,
        (rect.width - 4) * progress,
        rect.height - 4,
      );
      canvas.drawRect(fillRect, fillPaint);
    }
  }

  void _drawThermometer(Canvas canvas, Size size, Paint paint, Paint fillPaint) {
    final center = Offset(size.width / 2, size.height / 2);
    final bulbRadius = size.width * 0.25;
    final stemWidth = size.width * 0.15;
    
    // Draw stem
    final stemRect = Rect.fromLTWH(
      center.dx - stemWidth / 2,
      size.height * 0.15,
      stemWidth,
      size.height * 0.5,
    );
    canvas.drawRRect(
      RRect.fromRectAndRadius(stemRect, const Radius.circular(4)),
      paint,
    );

    // Draw bulb
    canvas.drawCircle(
      Offset(center.dx, stemRect.bottom + bulbRadius),
      bulbRadius,
      paint,
    );

    // Draw fill
    final fillHeight = stemRect.height * progress;
    final fillRect = Rect.fromLTWH(
      stemRect.left + 2,
      stemRect.bottom - fillHeight,
      stemRect.width - 4,
      fillHeight,
    );
    canvas.drawRRect(
      RRect.fromRectAndRadius(fillRect, const Radius.circular(2)),
      fillPaint,
    );
    canvas.drawCircle(
      Offset(center.dx, stemRect.bottom + bulbRadius),
      bulbRadius - 2,
      fillPaint,
    );
  }

  @override
  bool shouldRepaint(_StatusIconPainter oldDelegate) {
    return oldDelegate.progress != progress || oldDelegate.color != color;
  }
}