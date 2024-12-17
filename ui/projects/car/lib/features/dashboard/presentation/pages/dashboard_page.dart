import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../bloc/dashboard_bloc.dart';
import '../widgets/control_button.dart';
import '../widgets/status_card.dart';
import '../../domain/entities/vehicle_state.dart';
import '../../../../core/constants/control_icons.dart';

class DashboardPage extends StatelessWidget {
  const DashboardPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<DashboardBloc, DashboardState>(
      builder: (context, state) {
        if (state is DashboardLoading) {
          return const Center(child: CircularProgressIndicator());
        }
        
        if (state is DashboardError) {
          return Center(child: Text(state.message));
        }

        if (state is DashboardLoaded) {
          return DashboardView(vehicleState: state.vehicleState);
        }

        return const SizedBox();
      },
    );
  }
}

class DashboardView extends StatelessWidget {
  final VehicleState vehicleState;

  const DashboardView({
    super.key,
    required this.vehicleState,
  });

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
              _buildControlSection(context),
              const SizedBox(height: 24),
              _buildMonitoringSection(context),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildControlSection(BuildContext context) {
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
                isActive: vehicleState.engineOn,
                onChanged: (value) {
                  context.read<DashboardBloc>().add(
                    UpdateVehicleStateEvent(
                      vehicleState.copyWith(engineOn: value),
                    ),
                  );
                },
              ),
              ControlButton(
                label: 'Doors',
                svgString: ControlIcons.doorLock,
                isActive: vehicleState.doorsLocked,
                onChanged: (value) {
                  context.read<DashboardBloc>().add(
                    UpdateVehicleStateEvent(
                      vehicleState.copyWith(doorsLocked: value),
                    ),
                  );
                },
              ),
              ControlButton(
                label: 'Climate',
                svgString: ControlIcons.climateControl,
                isActive: vehicleState.climateControlOn,
                onChanged: (value) {
                  context.read<DashboardBloc>().add(
                    UpdateVehicleStateEvent(
                      vehicleState.copyWith(climateControlOn: value),
                    ),
                  );
                },
                temperature: vehicleState.climateTemp,
                onTemperatureChanged: (value) {
                  context.read<DashboardBloc>().add(
                    UpdateVehicleStateEvent(
                      vehicleState.copyWith(climateTemp: value),
                    ),
                  );
                },
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildMonitoringSection(BuildContext context) {
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
                onPressed: () => context.read<DashboardBloc>().add(GetVehicleStateEvent()),
                color: Colors.grey[600],
              ),
            ],
          ),
          const SizedBox(height: 24),
          Row(
            children: [
              Expanded(
                child: StatusCard(
                  label: 'Speed',
                  value: vehicleState.speed,
                  maxValue: 200,
                  type: StatusType.speed,
                  unit: ' km/h',
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: StatusCard(
                  label: 'Fuel Level',
                  value: vehicleState.fuelLevel,
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
                child: StatusCard(
                  label: 'Battery Level',
                  value: vehicleState.batteryLevel,
                  type: StatusType.battery,
                  unit: '%',
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: StatusCard(
                  label: 'Temperature',
                  value: vehicleState.temperature,
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