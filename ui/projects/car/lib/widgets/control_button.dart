import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';

class ControlButton extends StatelessWidget {
  final String label;
  final String svgString;
  final bool isActive;
  final Function(bool) onChanged;
  final double? temperature;
  final Function(double)? onTemperatureChanged;

  const ControlButton({
    Key? key,
    required this.label,
    required this.svgString,
    required this.isActive,
    required this.onChanged,
    this.temperature,
    this.onTemperatureChanged,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          width: 80,
          height: 80,
          decoration: BoxDecoration(
            color: isActive ? Colors.blue.withOpacity(0.1) : Colors.grey[100],
            borderRadius: BorderRadius.circular(20),
          ),
          child: Material(
            color: Colors.transparent,
            child: InkWell(
              borderRadius: BorderRadius.circular(20),
              onTap: () => onChanged(!isActive),
              child: Center(
                child: SvgPicture.string(
                  svgString,
                  width: 36,
                  height: 36,
                  colorFilter: ColorFilter.mode(
                    isActive ? Colors.blue : Colors.grey,
                    BlendMode.srcIn,
                  ),
                ),
              ),
            ),
          ),
        ),
        const SizedBox(height: 8),
        Text(
          label,
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w500,
            color: isActive ? Colors.blue : Colors.grey[600],
          ),
        ),
        if (temperature != null && onTemperatureChanged != null && isActive)
          Padding(
            padding: const EdgeInsets.only(top: 8),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(
                  Icons.thermostat,
                  size: 16,
                  color: Colors.grey[600],
                ),
                const SizedBox(width: 4),
                Text(
                  '${temperature!.round()}°C',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.grey[600],
                  ),
                ),
              ],
            ),
          ),
      ],
    );
  }
}