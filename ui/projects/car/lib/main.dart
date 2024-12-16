import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:car/control_button.dart';
import 'package:car/dashboard_row.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Car Instrument Cluster',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blueGrey),
        useMaterial3: true,
      ),
      home: const MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key});

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  void _showSnackBar(String message) {
    debugPrint('Showing SnackBar: $message'); // Debug print
    ScaffoldMessenger.of(context).removeCurrentSnackBar();
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message)),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Instrument Cluster'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            DashboardRow(
              icon1: Icons.speed,
              value1: '120 km/h',
              icon2: Icons.settings,
              value2: '3000',
            ),
            DashboardRow(
              icon1: Icons.local_gas_station,
              value1: '75%',
              icon2: Icons.battery_full,
              value2: '80%',
            ),
            ControlPanel(showSnackBar: _showSnackBar),
          ],
        ),
      ),
    );
  }
}

class ControlPanel extends StatefulWidget {
  final void Function(String) showSnackBar;

  const ControlPanel({required this.showSnackBar, super.key});

  @override
  State<ControlPanel> createState() => _ControlPanelState();
}

class _ControlPanelState extends State<ControlPanel> {
  bool _engineStarted = false;
  bool _doorsLocked = false;
  bool _hornHonked = false;
  bool _climateAdjusted = false;
  bool _sunroofOpen = false;
  bool _headlightsOn = false;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            ControlButton(
              assetOn: 'lib/assets/power.svg',
              assetOff: 'lib/assets/start_engine.svg',
              label: 'Start Engine',
              initialState: _engineStarted,
              onToggle: (isOn) {
                setState(() {
                  _engineStarted = isOn;
                });
                widget.showSnackBar(isOn ? 'Engine started' : 'Engine stopped');
              },
            ),
            ControlButton(
              assetOn: 'lib/assets/lock.svg',
              assetOff: 'lib/assets/unlock.svg',
              label: 'Lock Doors',
              initialState: _doorsLocked,
              onToggle: (isOn) {
                setState(() {
                  _doorsLocked = isOn;
                });
                widget.showSnackBar(isOn ? 'Doors locked' : 'Doors unlocked');
              },
            ),
          ],
        ),
        const SizedBox(height: 16),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            ControlButton(
              assetOn: 'lib/assets/honk.svg',
              assetOff: 'lib/assets/mute.svg',
              label: 'Honk Horn',
              initialState: _hornHonked,
              onToggle: (isOn) {
                setState(() {
                  _hornHonked = isOn;
                });
                widget.showSnackBar(isOn ? 'Horn honked' : 'Horn stopped');
              },
            ),
            ControlButton(
              assetOn: 'lib/assets/climate_on.svg',
              assetOff: 'lib/assets/adjust_climate.svg',
              label: 'Adjust Climate',
              initialState: _climateAdjusted,
              onToggle: (isOn) {
                setState(() {
                  _climateAdjusted = isOn;
                });
                widget.showSnackBar(isOn ? 'Climate control adjusted' : 'Climate control stopped');
              },
            ),
          ],
        ),
        const SizedBox(height: 16),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            ControlButton(
              assetOn: 'lib/assets/sunroof_open.svg',
              assetOff: 'lib/assets/sunroof.svg',
              label: 'Sunroof',
              initialState: _sunroofOpen,
              onToggle: (isOn) {
                setState(() {
                  _sunroofOpen = isOn;
                });
                widget.showSnackBar(isOn ? 'Sunroof opened' : 'Sunroof closed');
              },
            ),
            ControlButton(
              assetOn: 'lib/assets/headlights.svg',
              assetOff: 'lib/assets/headlights_off.svg',
              label: 'Headlights',
              initialState: _headlightsOn,
              onToggle: (isOn) {
                setState(() {
                  _headlightsOn = isOn;
                });
                widget.showSnackBar(isOn ? 'Headlights on' : 'Headlights off');
              },
            ),
          ],
        ),
      ],
    );
  }
}
