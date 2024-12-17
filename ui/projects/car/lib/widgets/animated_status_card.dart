import 'package:flutter/material.dart';

class AnimatedStatusCard extends StatelessWidget {
  final String title;
  final double value;
  final double maxValue;
  final IconData icon;
  final Color color;
  final String unit;

  const AnimatedStatusCard({
    Key? key,
    required this.title,
    required this.value,
    this.maxValue = 100,
    required this.icon,
    required this.color,
    required this.unit,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.1),
            spreadRadius: 0,
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: color.withOpacity(0.1),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Icon(
              icon,
              color: color,
              size: 24,
            ),
          ),
          TweenAnimationBuilder<double>(
            duration: const Duration(milliseconds: 500),
            tween: Tween(begin: 0, end: value),
            curve: Curves.easeOutCubic,
            builder: (context, value, _) {
              return Text(
                '${value.toStringAsFixed(1)}$unit',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.w600,
                  color: color,
                ),
              );
            },
          ),
        ],
      ),
    );
  }
}