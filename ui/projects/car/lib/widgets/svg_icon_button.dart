import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';

class SvgIconButton extends StatelessWidget {
  final String svgString;
  final bool isActive;
  final VoidCallback onPressed;
  final double size;

  const SvgIconButton({
    Key? key,
    required this.svgString,
    required this.isActive,
    required this.onPressed,
    this.size = 64,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onPressed,
      child: Container(
        width: size,
        height: size,
        decoration: BoxDecoration(
          color: isActive ? Colors.blue.withOpacity(0.1) : Colors.transparent,
          borderRadius: BorderRadius.circular(12),
        ),
        child: SvgPicture.string(
          svgString,
          width: size * 0.8,
          height: size * 0.8,
          colorFilter: ColorFilter.mode(
            isActive ? Colors.blue : Colors.grey,
            BlendMode.srcIn,
          ),
        ),
      ),
    );
  }
}
