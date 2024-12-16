import 'package:flutter/material.dart';
import '../models/vehicle_state.dart';
import '../widgets/control_icons.dart';
import '../widgets/active_state_animations.dart';

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
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Vehicle Status',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 16),
            _buildStatusTile(
              'Speed',
              '${_vehicleState.speed.round()} km/h',
              Icons.speed,
            ),
            _buildStatusTile(
              'Fuel Level',
              '${_vehicleState.fuelLevel.round()}%',
              Icons.local_gas_station,
            ),
            _buildStatusTile(
              'Battery Level',
              '${_vehicleState.batteryLevel.round()}%',
              Icons.battery_full,
            ),
            _buildStatusTile(
              'Temperature',
              '${_vehicleState.temperature.round()}°C',
              Icons.thermostat,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatusTile(String title, String value, IconData icon) {
    return ListTile(
      leading: Icon(icon),
      title: Text(title),
      trailing: Text(
        value,
        style: const TextStyle(
          fontSize: 18,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}
