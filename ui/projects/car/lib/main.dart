import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';

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
            Column(
              children: [
                ElevatedButton(
                  onPressed: () {
                    setState(() {
                      _engineStarted = !_engineStarted;
                    });
                    widget.showSnackBar(_engineStarted ? 'Engine started' : 'Engine stopped');
                  },
                  child: SvgPicture.asset(
                    _engineStarted ? 'lib/assets/power.svg' : 'lib/assets/start_engine.svg',
                    width: 24,
                    height: 24,
                  ),
                ),
                const SizedBox(height: 4),
                const Text('Start Engine', style: TextStyle(fontSize: 12)),
              ],
            ),
            Column(
              children: [
                ElevatedButton(
                  onPressed: () {
                    setState(() {
                      _doorsLocked = !_doorsLocked;
                    });
                    widget.showSnackBar(_doorsLocked ? 'Doors locked' : 'Doors unlocked');
                  },
                  child: SvgPicture.asset(
                    _doorsLocked ? 'lib/assets/lock.svg' : 'lib/assets/unlock.svg',
                    width: 24,
                    height: 24,
                  ),
                ),
                const SizedBox(height: 4),
                const Text('Lock Doors', style: TextStyle(fontSize: 12)),
              ],
            ),
          ],
        ),
        const SizedBox(height: 16),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            Column(
              children: [
                ElevatedButton(
                  onPressed: () {
                    setState(() {
                      _hornHonked = !_hornHonked;
                    });
                    widget.showSnackBar(_hornHonked ? 'Horn honked' : 'Horn stopped');
                  },
                  child: SvgPicture.asset(
                    _hornHonked ? 'lib/assets/honk.svg' : 'lib/assets/mute.svg',
                    width: 24,
                    height: 24,
                  ),
                ),
                const SizedBox(height: 4),
                const Text('Honk Horn', style: TextStyle(fontSize: 12)),
              ],
            ),
            Column(
              children: [
                ElevatedButton(
                  onPressed: () {
                    setState(() {
                      _climateAdjusted = !_climateAdjusted;
                    });
                    widget.showSnackBar(_climateAdjusted ? 'Climate control adjusted' : 'Climate control stopped');
                  },
                  child: SvgPicture.asset(
                    _climateAdjusted ? 'lib/assets/climate_on.svg' : 'lib/assets/adjust_climate.svg',
                    width: 24,
                    height: 24,
                  ),
                ),
                const SizedBox(height: 4),
                const Text('Adjust Climate', style: TextStyle(fontSize: 12)),
              ],
            ),
          ],
        ),
        const SizedBox(height: 16),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            Column(
              children: [
                ElevatedButton(
                  onPressed: () {
                    setState(() {
                      _sunroofOpen = !_sunroofOpen;
                    });
                    widget.showSnackBar(_sunroofOpen ? 'Sunroof opened' : 'Sunroof closed');
                  },
                  child: SvgPicture.asset(
                    _sunroofOpen ? 'lib/assets/sunroof_open.svg' : 'lib/assets/sunroof.svg',
                    width: 24,
                    height: 24,
                  ),
                ),
                const SizedBox(height: 4),
                const Text('Sunroof', style: TextStyle(fontSize: 12)),
              ],
            ),
            Column(
              children: [
                ElevatedButton(
                  onPressed: () {
                    setState(() {
                      _headlightsOn = !_headlightsOn;
                    });
                    widget.showSnackBar(_headlightsOn ? 'Headlights on' : 'Headlights off');
                  },
                  child: SvgPicture.asset(
                    _headlightsOn ? 'lib/assets/headlights.svg' : 'lib/assets/headlights_off.svg',
                    width: 24,
                    height: 24,
                  ),
                ),
                const SizedBox(height: 4),
                const Text('Headlights', style: TextStyle(fontSize: 12)),
              ],
            ),
          ],
        ),
      ],
    );
  }
}
