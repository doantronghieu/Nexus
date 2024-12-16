import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';

class ControlButton extends StatefulWidget {
  final String assetOn;
  final String assetOff;
  final String label;
  final void Function(bool) onToggle;
  final bool initialState;

  const ControlButton({
    super.key,
    required this.assetOn,
    required this.assetOff,
    required this.label,
    required this.onToggle,
    this.initialState = false,
  });

  @override
  State<ControlButton> createState() => _ControlButtonState();
}

class _ControlButtonState extends State<ControlButton> {
  late bool _isOn;

  @override
  void initState() {
    super.initState();
    _isOn = widget.initialState;
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        ElevatedButton(
          onPressed: () {
            setState(() {
              _isOn = !_isOn;
            });
            widget.onToggle(_isOn);
          },
          child: SvgPicture.asset(
            _isOn ? widget.assetOn : widget.assetOff,
            width: 24,
            height: 24,
          ),
        ),
        const SizedBox(height: 4),
        Text(widget.label, style: const TextStyle(fontSize: 12)),
      ],
    );
  }
}
