import 'package:flutter/material.dart';
import '../models/vehicle_state.dart';
import '../widgets/control_icons.dart';
import '../widgets/active_state_animations.dart';
import '../widgets/animated_status_card.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  VehicleState _vehicleState = VehicleState();

  void _updateVehicleState(VehicleState newState) {
    setState(() {
      _vehicleState = newState;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[100],
      appBar: AppBar(
        title: const Text('Vehicle Control Dashboard'),
        backgroundColor: Colors.blue,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildControlSection(),
            const SizedBox(height: 20),
            _buildMonitoringSection(),
          ],
        ),
      ),
    );
  }

  Widget _buildControlSection() {
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Controls',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _buildControlButton(
                  'Engine',
                  ControlIcons.engineControl,
                  _vehicleState.engineOn,
                  (value) {
                    _updateVehicleState(_vehicleState.copyWith(engineOn: value));
                  },
                ),
                _buildControlButton(
                  'Doors',
                  ControlIcons.doorLock,
                  _vehicleState.doorsLocked,
                  (value) {
                    _updateVehicleState(_vehicleState.copyWith(doorsLocked: value));
                  },
                ),
                _buildControlButton(
                  'Climate',
                  ControlIcons.climateControl,
                  _vehicleState.climateControlOn,
                  (value) {
                    _updateVehicleState(
                        _vehicleState.copyWith(climateControlOn: value));
                  },
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildControlButton(
    String label,
    String svgString,
    bool isActive,
    Function(bool) onChanged,
  ) {
    String type = label.toLowerCase();
    return Column(
      children: [
        ActiveStateButton(
          svgString: svgString,
          isActive: isActive,
          onPressed: () => onChanged(!isActive),
          type: type,
          temperature: _vehicleState.climateTemp,
          onTemperatureChanged: type == 'climate'
              ? (value) {
                  _updateVehicleState(
                    _vehicleState.copyWith(climateTemp: value),
                  );
                }
              : null,
        ),
        const SizedBox(height: 8),
        AnimatedDefaultTextStyle(
          duration: const Duration(milliseconds: 200),
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
            color: isActive ? Colors.blue : Colors.grey,
          ),
          child: Text(label),
        ),
      ],
    );
  }

  Widget _buildMonitoringSection() {
    return Container(
      padding: const EdgeInsets.all(24.0),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(24),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.1),
            spreadRadius: 0,
            blurRadius: 16,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                'Vehicle Status',
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                ),
              ),
              IconButton(
                icon: const Icon(Icons.refresh),
                onPressed: () {},
                color: Colors.grey[600],
              ),
            ],
          ),
          const SizedBox(height: 24),
          Row(
            children: [
              Expanded(
                child: AnimatedStatusCard(
                  title: 'Speed',
                  value: _vehicleState.speed,
                  maxValue: 200,
                  icon: Icons.speed,
                  color: Colors.blue,
                  unit: ' km/h',
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: AnimatedStatusCard(
                  title: 'Fuel Level',
                  value: _vehicleState.fuelLevel,
                  icon: Icons.local_gas_station,
                  color: Colors.green,
                  unit: '%',
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              Expanded(
                child: AnimatedStatusCard(
                  title: 'Battery Level',
                  value: _vehicleState.batteryLevel,
                  icon: Icons.battery_full,
                  color: Colors.orange,
                  unit: '%',
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: AnimatedStatusCard(
                  title: 'Temperature',
                  value: _vehicleState.temperature,
                  maxValue: 50,
                  icon: Icons.thermostat,
                  color: Colors.red,
                  unit: '°C',
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}