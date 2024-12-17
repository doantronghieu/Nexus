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
    return Card(
      elevation: 2,
      child: Tooltip(
        message: title,
        child: TweenAnimationBuilder<double>(
          duration: const Duration(milliseconds: 800),
          tween: Tween(begin: 0, end: value),
          curve: Curves.easeOutCubic,
          builder: (context, animatedValue, _) {
            return Container(
              padding: const EdgeInsets.all(12),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  // Icon with background
                  Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: color.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Icon(
                      icon, 
                      color: color,
                      size: 24,
                    ),
                  ),
                  
                  const SizedBox(width: 16),
                  
                  // Progress bar
                  Expanded(
                    child: Stack(
                      children: [
                        Container(
                          height: 4,
                          decoration: BoxDecoration(
                            color: Colors.grey.shade200,
                            borderRadius: BorderRadius.circular(2),
                          ),
                        ),
                        AnimatedContainer(
                          duration: const Duration(milliseconds: 500),
                          height: 4,
                          width: (animatedValue / maxValue) * 100,
                          decoration: BoxDecoration(
                            color: color,
                            borderRadius: BorderRadius.circular(2),
                          ),
                        ),
                      ],
                    ),
                  ),
                  
                  const SizedBox(width: 16),
                  
                  // Value with animation
                  TweenAnimationBuilder<double>(
                    duration: const Duration(milliseconds: 800),
                    tween: Tween(begin: 0, end: value),
                    curve: Curves.easeOutCubic,
                    builder: (context, value, _) {
                      return SizedBox(
                        width: unit.contains('km/h') ? 90 : 70, // Wider for km/h
                        child: Text(
                          '${value.toStringAsFixed(1)}$unit',
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                            color: color,
                          ),
                          textAlign: TextAlign.end,
                          softWrap: false,
                          overflow: TextOverflow.visible,
                        ),
                      );
                    },
                  ),
                ],
              ),
            );
          },
        ),
      ),
    );
  }
}