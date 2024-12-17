import 'package:flutter/material.dart';

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