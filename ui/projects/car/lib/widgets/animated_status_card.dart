import 'package:flutter/material.dart';

enum StatusType { speed, fuel, battery, temperature }

class AnimatedStatusCard extends StatelessWidget {
  final String label;
  final double value;
  final double maxValue;
  final StatusType type;
  final String unit;

  const AnimatedStatusCard({
    Key? key,
    required this.label,
    required this.value,
    this.maxValue = 100,
    required this.type,
    required this.unit,
  }) : super(key: key);

  Color get color {
    switch (type) {
      case StatusType.speed:
        return Colors.blue;
      case StatusType.fuel:
        return Colors.green;
      case StatusType.battery:
        return Colors.orange;
      case StatusType.temperature:
        return Colors.red;
    }
  }

  IconData get icon {
    switch (type) {
      case StatusType.speed:
        return Icons.speed;
      case StatusType.fuel:
        return Icons.local_gas_station;
      case StatusType.battery:
        return Icons.battery_full;
      case StatusType.temperature:
        return Icons.thermostat;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            spreadRadius: 0,
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
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
          const Spacer(),
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