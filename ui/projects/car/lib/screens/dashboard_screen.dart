import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import '../models/vehicle_state.dart';
import '../widgets/control_icons.dart';
import '../widgets/svg_icon_button.dart';

class DashboardScreen extends StatefulWidget {
  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  VehicleState _vehicleState = VehicleState();

  void _updateVehicleState(VehicleState newState) {
    setState(() {
      _vehicleState = newState;
    });
    // Here you would typically send the update to your backend
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Vehicle Control Dashboard'),
        backgroundColor: Colors.blue,
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildControlSection(),
            SizedBox(height: 20),
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
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Controls',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _buildControlButton(
                  'Engine',
                  ControlIcons.engineControl,
                  _vehicleState.engineOn,
                  (value) {
                    _updateVehicleState(
                        _vehicleState.copyWith(engineOn: value));
                  },
                ),
                _buildControlButton(
                  'Doors',
                  ControlIcons.doorLock,
                  _vehicleState.doorsLocked,
                  (value) {
                    _updateVehicleState(
                        _vehicleState.copyWith(doorsLocked: value));
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
            if (_vehicleState.climateControlOn) _buildClimateSlider(),
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
    return Column(
      children: [
        SvgIconButton(
          svgString: svgString,
          isActive: isActive,
          onPressed: () => onChanged(!isActive),
        ),
        SizedBox(height: 8),
        Text(
          label,
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w500,
            color: isActive ? Colors.blue : Colors.grey,
          ),
        ),
      ],
    );
  }

  Widget _buildClimateSlider() {
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Temperature: ${_vehicleState.climateTemp.round()}°C',
            style: TextStyle(fontSize: 16),
          ),
          Slider(
            value: _vehicleState.climateTemp,
            min: 16,
            max: 30,
            divisions: 28,
            label: '${_vehicleState.climateTemp.round()}°C',
            onChanged: (value) {
              _updateVehicleState(
                _vehicleState.copyWith(climateTemp: value),
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildMonitoringSection() {
    return Card(
      elevation: 4,
      child: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Vehicle Status',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 16),
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
        style: TextStyle(
          fontSize: 18,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}
