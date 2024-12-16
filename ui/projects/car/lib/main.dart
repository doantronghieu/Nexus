import 'package:flutter/material.dart';

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
            _buildDashboardRow(Icons.speed, '120 km/h', Icons.settings, '3000'),
            _buildDashboardRow(Icons.local_gas_station, '75%', Icons.battery_full, '80%'),
            ControlPanel(showSnackBar: _showSnackBar),
          ],
        ),
      ),
    );
  }

  Widget _buildDashboardRow(IconData icon1, String value1, IconData icon2, String value2) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceAround,
      children: [
        _buildDashboardItem(icon1, value1),
        _buildDashboardItem(icon2, value2),
      ],
    );
  }

  Widget _buildDashboardItem(IconData icon, String value) {
    return Column(
      children: [
        Icon(
          icon,
          size: 40,
          color: Colors.blueGrey,
        ),
        const SizedBox(height: 8),
        Text(
          value,
          style: const TextStyle(fontSize: 24, color: Colors.blueGrey),
        ),
      ],
    );
  }
}

class ControlPanel extends StatelessWidget {
  final void Function(String) showSnackBar;

  const ControlPanel({required this.showSnackBar, super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            ElevatedButton(
              onPressed: () {
                showSnackBar('Engine started');
              },
              child: const Text('Start Engine'),
            ),
            ElevatedButton(
              onPressed: () {
                showSnackBar('Doors locked');
              },
              child: const Text('Lock Doors'),
            ),
          ],
        ),
        const SizedBox(height: 16),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            ElevatedButton(
              onPressed: () {
                showSnackBar('Horn honked');
              },
              child: const Text('Honk Horn'),
            ),
            ElevatedButton(
              onPressed: () {
                showSnackBar('Climate control adjusted');
              },
              child: const Text('Adjust Climate'),
            ),
          ],
        ),
        const SizedBox(height: 16),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            ElevatedButton(
              onPressed: () {
                showSnackBar('Sunroof opened/closed');
              },
              child: const Text('Sunroof'),
            ),
            ElevatedButton(
              onPressed: () {
                showSnackBar('Headlights on/off');
              },
              child: const Text('Headlights'),
            ),
          ],
        ),
      ],
    );
  }
}
