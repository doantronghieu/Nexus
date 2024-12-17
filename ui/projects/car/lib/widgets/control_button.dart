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
    bool isClimate = label.toLowerCase() == 'climate';

    return Column(
      children: [
        GestureDetector(
          onTapDown: isClimate && isActive ? 
            (TapDownDetails details) => _showTemperatureControl(context) : null,
          child: Container(
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
                child: Stack(
                  alignment: Alignment.center,
                  children: [
                    SvgPicture.string(
                      svgString,
                      width: 36,
                      height: 36,
                      colorFilter: ColorFilter.mode(
                        isActive ? Colors.blue : Colors.grey,
                        BlendMode.srcIn,
                      ),
                    ),
                    if (temperature != null && isActive && isClimate)
                      Positioned(
                        bottom: 8,
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Icon(
                              Icons.thermostat,
                              size: 12,
                              color: Colors.blue,
                            ),
                            Text(
                              '${temperature!.round()}°C',
                              style: TextStyle(
                                fontSize: 12,
                                fontWeight: FontWeight.w500,
                                color: Colors.blue,
                              ),
                            ),
                          ],
                        ),
                      ),
                  ],
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
      ],
    );
  }

  void _showTemperatureControl(BuildContext context) {
    if (onTemperatureChanged == null || temperature == null) return;

    double tempValue = temperature!;

    showDialog(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setState) {
          return AlertDialog(
            title: const Text('Set Temperature'),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  '${tempValue.round()}°C',
                  style: const TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Slider(
                  value: tempValue,
                  min: 16,
                  max: 30,
                  divisions: 28,
                  label: '${tempValue.round()}°C',
                  onChanged: (value) {
                    setState(() {
                      tempValue = value;
                    });
                    onTemperatureChanged!(value);
                  },
                ),
              ],
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.of(context).pop(),
                child: const Text('Close'),
              ),
            ],
          );
        },
      ),
    );
  }
}