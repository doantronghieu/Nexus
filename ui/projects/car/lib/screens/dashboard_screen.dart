import 'package:flutter/material.dart';
import '../models/vehicle_state.dart';
import '../widgets/control_icons.dart';
import '../widgets/active_state_animations.dart';
import '../widgets/animated_status_card.dart';
import '../widgets/control_button.dart';

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
      backgroundColor: const Color(0xFFF5F5F5),
      appBar: AppBar(
        title: const Text(
          'Vehicle Control Dashboard',
          style: TextStyle(
            fontSize: 22,
            fontWeight: FontWeight.w500,
            color: Colors.white,
          ),
        ),
        backgroundColor: Colors.blue,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 24.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _buildControlSection(),
              const SizedBox(height: 24),
              _buildMonitoringSection(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildControlSection() {
    return Container(
      padding: const EdgeInsets.all(24.0),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(24),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 16,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Controls',
            style: TextStyle(
              fontSize: 28,
              fontWeight: FontWeight.w600,
              color: Colors.black,
            ),
          ),
          const SizedBox(height: 24),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              ControlButton(
                label: 'Engine',
                svgString: ControlIcons.engineControl,
                isActive: _vehicleState.engineOn,
                onChanged: (value) {
                  _updateVehicleState(_vehicleState.copyWith(engineOn: value));
                },
              ),
              ControlButton(
                label: 'Doors',
                svgString: ControlIcons.doorLock,
                isActive: _vehicleState.doorsLocked,
                onChanged: (value) {
                  _updateVehicleState(_vehicleState.copyWith(doorsLocked: value));
                },
              ),
              ControlButton(
                label: 'Climate',
                svgString: ControlIcons.climateControl,
                isActive: _vehicleState.climateControlOn,
                onChanged: (value) {
                  _updateVehicleState(_vehicleState.copyWith(climateControlOn: value));
                },
                temperature: _vehicleState.climateTemp,
                onTemperatureChanged: (value) {
                  _updateVehicleState(_vehicleState.copyWith(climateTemp: value));
                },
              ),
            ],
          ),
        ],
      ),
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
            color: Colors.black.withOpacity(0.05),
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
                  fontWeight: FontWeight.w600,
                  color: Colors.black,
                ),
              ),
              IconButton(
                icon: const Icon(Icons.refresh, size: 28),
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
                  label: 'Speed',
                  value: _vehicleState.speed,
                  maxValue: 200,
                  type: StatusType.speed,
                  unit: ' km/h',
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: AnimatedStatusCard(
                  label: 'Fuel Level',
                  value: _vehicleState.fuelLevel,
                  type: StatusType.fuel,
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
                  label: 'Battery Level',
                  value: _vehicleState.batteryLevel,
                  type: StatusType.battery,
                  unit: '%',
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: AnimatedStatusCard(
                  label: 'Temperature',
                  value: _vehicleState.temperature,
                  maxValue: 50,
                  type: StatusType.temperature,
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