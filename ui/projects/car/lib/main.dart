import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'features/dashboard/presentation/bloc/dashboard_bloc.dart';
import 'features/dashboard/presentation/pages/dashboard_page.dart';
import 'core/di/injection_container.dart' as di;

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await di.init();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Vehicle Control',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: BlocProvider(
        create: (_) => di.sl<DashboardBloc>()..add(GetVehicleStateEvent()),
        child: const DashboardPage(),
      ),
    );
  }
}