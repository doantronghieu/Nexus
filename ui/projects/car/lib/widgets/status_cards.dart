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
      child: TweenAnimationBuilder<double>(
        duration: const Duration(milliseconds: 800),
        tween: Tween(begin: 0, end: value),
        curve: Curves.easeOutCubic,
        builder: (context, value, _) {
          return Container(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Icon(icon, color: color),
                    const SizedBox(width: 8),
                    Text(
                      title,
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                Stack(
                  children: [
                    Container(
                      height: 4,
                      width: double.infinity,
                      decoration: BoxDecoration(
                        color: Colors.grey.shade200,
                        borderRadius: BorderRadius.circular(2),
                      ),
                    ),
                    AnimatedContainer(
                      duration: const Duration(milliseconds: 500),
                      height: 4,
                      width: (value / maxValue) * (MediaQuery.of(context).size.width - 64),
                      decoration: BoxDecoration(
                        color: color,
                        borderRadius: BorderRadius.circular(2),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                Row(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    TweenAnimationBuilder<double>(
                      duration: const Duration(milliseconds: 800),
                      tween: Tween(begin: 0, end: value),
                      curve: Curves.easeOutCubic,
                      builder: (context, value, _) {
                        return Text(
                          '${value.toStringAsFixed(1)}$unit',
                          style: TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                            color: color,
                          ),
                        );
                      },
                    ),
                  ],
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}

class StatusChangeIndicator extends StatelessWidget {
  final Widget child;
  final double oldValue;
  final double newValue;

  const StatusChangeIndicator({
    Key? key,
    required this.child,
    required this.oldValue,
    required this.newValue,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        child,
        if (oldValue != newValue)
          Positioned(
            right: 0,
            child: TweenAnimationBuilder<double>(
              duration: const Duration(milliseconds: 300),
              tween: Tween(begin: 0, end: 1),
              builder: (context, value, child) {
                return Transform.translate(
                  offset: Offset(0, -10 * value),
                  child: Opacity(
                    opacity: 1 - value,
                    child: Icon(
                      newValue > oldValue
                          ? Icons.arrow_upward
                          : Icons.arrow_downward,
                      color: newValue > oldValue ? Colors.green : Colors.red,
                      size: 16,
                    ),
                  ),
                );
              },
            ),
          ),
      ],
    );
  }
}