import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'dart:math' as math;

class ActiveStateButton extends StatefulWidget {
  final String svgString;
  final bool isActive;
  final VoidCallback onPressed;
  final String type;
  final double size;
  final double temperature;
  final ValueChanged<double>? onTemperatureChanged;

  const ActiveStateButton({
    super.key,
    required this.svgString,
    required this.isActive,
    required this.onPressed,
    required this.type,
    required this.temperature,
    this.onTemperatureChanged,
    this.size = 64,
  });

  @override
  State<ActiveStateButton> createState() => _ActiveStateButtonState();
}

class _ActiveStateButtonState extends State<ActiveStateButton>
    with TickerProviderStateMixin {
  late AnimationController _pulseController;
  late AnimationController _rotateController;
  late Animation<double> _scaleAnimation;
  late Animation<double> _rotationAnimation;
  final List<AnimationController> _waveControllers = [];
  final List<Animation<double>> _waveAnimations = [];
  bool _showTemperatureControl = false;

  @override
  void initState() {
    super.initState();
    _initializeAnimations();
    if (widget.isActive) {
      _startAnimations();
    }
  }

  void _initializeAnimations() {
    _pulseController = AnimationController(
      duration: const Duration(milliseconds: 500),
      vsync: this,
    );
    _scaleAnimation = TweenSequence<double>([
      TweenSequenceItem(tween: Tween(begin: 1.0, end: 1.02), weight: 1),
      TweenSequenceItem(tween: Tween(begin: 1.02, end: 0.98), weight: 1),
      TweenSequenceItem(tween: Tween(begin: 0.98, end: 1.0), weight: 1),
    ]).animate(_pulseController);

    _rotateController = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    );
    _rotationAnimation = Tween<double>(
      begin: 0,
      end: 2 * math.pi,
    ).animate(_rotateController);

    for (int i = 0; i < 3; i++) {
      final controller = AnimationController(
        duration: Duration(milliseconds: 1500 + (i * 300)),
        vsync: this,
      );
      _waveControllers.add(controller);
      _waveAnimations.add(
        Tween<double>(begin: 0, end: 1).animate(
          CurvedAnimation(parent: controller, curve: Curves.easeInOut),
        ),
      );
    }
  }

  @override
  void dispose() {
    _pulseController.dispose();
    _rotateController.dispose();
    for (final controller in _waveControllers) {
      controller.dispose();
    }
    super.dispose();
  }

  @override
  void didUpdateWidget(ActiveStateButton oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.isActive != oldWidget.isActive) {
      if (widget.isActive) {
        _startAnimations();
      } else {
        _stopAnimations();
      }
    }
  }

  void _startAnimations() {
    if (widget.type == 'engine') {
      _pulseController.repeat();
    } else if (widget.type == 'climate') {
      _rotateController.repeat();
      for (final controller in _waveControllers) {
        controller.repeat();
      }
    }
  }

  void _stopAnimations() {
    _pulseController.stop();
    _rotateController.stop();
    for (final controller in _waveControllers) {
      controller.stop();
    }
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        if (widget.type == 'climate' && widget.isActive) {
          setState(() {
            _showTemperatureControl = !_showTemperatureControl;
          });
        } else {
          widget.onPressed();
        }
      },
      onLongPress: widget.type == 'climate' ? widget.onPressed : null,
      child: Container(
        width: widget.size,
        height: widget.size,
        decoration: BoxDecoration(
          color: widget.isActive
              ? Colors.blue.withOpacity(0.1)
              : Colors.transparent,
          borderRadius: BorderRadius.circular(12),
        ),
        child: Stack(
          alignment: Alignment.center,
          children: [
            if (widget.type == 'engine' && widget.isActive)
              _buildEngineAnimation(),
            if (widget.type == 'climate' && widget.isActive)
              _buildClimateAnimation(),
            if (widget.type == 'door' && widget.isActive) _buildDoorAnimation(),
            SvgPicture.string(
              widget.svgString,
              width: widget.size * 0.8,
              height: widget.size * 0.8,
              colorFilter: ColorFilter.mode(
                widget.isActive ? Colors.blue : Colors.grey,
                BlendMode.srcIn,
              ),
            ),
            if (widget.type == 'climate' &&
                widget.isActive &&
                _showTemperatureControl)
              _buildTemperatureControl(),
          ],
        ),
      ),
    );
  }

  Widget _buildEngineAnimation() {
    return AnimatedBuilder(
      animation: _pulseController,
      builder: (context, child) {
        return Transform.scale(
          scale: _scaleAnimation.value,
          child: Container(
            width: widget.size * 0.9,
            height: widget.size * 0.9,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              border: Border.all(
                color: Colors.blue.withOpacity(0.3),
                width: 2,
              ),
            ),
          ),
        );
      },
    );
  }

  Widget _buildClimateAnimation() {
    return Stack(
      children: _waveAnimations.map((animation) {
        return AnimatedBuilder(
          animation: animation,
          builder: (context, child) {
            return Opacity(
              opacity: (1 - animation.value) * 0.5,
              child: Transform.scale(
                scale: 0.5 + (animation.value * 0.5),
                child: Container(
                  width: widget.size,
                  height: widget.size,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    border: Border.all(
                      color: Colors.blue.withOpacity(0.3),
                      width: 2,
                    ),
                  ),
                ),
              ),
            );
          },
        );
      }).toList(),
    );
  }

  Widget _buildDoorAnimation() {
    return TweenAnimationBuilder(
      tween: Tween<double>(begin: 0, end: 1),
      duration: const Duration(milliseconds: 500),
      builder: (context, double value, child) {
        return Container(
          width: widget.size * 0.9,
          height: widget.size * 0.9,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(8),
            border: Border.all(
              color: Colors.blue.withOpacity(0.3 * value),
              width: 2,
            ),
          ),
        );
      },
    );
  }

  Widget _buildTemperatureControl() {
    return Container(
      width: widget.size,
      height: widget.size,
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.9),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min, // Added this
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          SizedBox(
            // Wrapped in SizedBox with constrained height
            height: widget.size * 0.3,
            child: IconButton(
              padding: EdgeInsets.zero, // Remove padding
              iconSize: widget.size * 0.2, // Scale icon size
              icon: const Icon(Icons.add),
              onPressed: () {
                widget.onTemperatureChanged
                    ?.call((widget.temperature + 0.5).clamp(16.0, 30.0));
              },
            ),
          ),
          SizedBox(
            // Wrapped temperature display in SizedBox
            height: widget.size * 0.3,
            child: Center(
              child: Text(
                '${widget.temperature.toStringAsFixed(1)}°C',
                style: TextStyle(
                  fontSize: widget.size * 0.2, // Scale font size
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
          SizedBox(
            // Wrapped in SizedBox with constrained height
            height: widget.size * 0.3,
            child: IconButton(
              padding: EdgeInsets.zero, // Remove padding
              iconSize: widget.size * 0.2, // Scale icon size
              icon: const Icon(Icons.remove),
              onPressed: () {
                widget.onTemperatureChanged
                    ?.call((widget.temperature - 0.5).clamp(16.0, 30.0));
              },
            ),
          ),
        ],
      ),
    );
  }
}
