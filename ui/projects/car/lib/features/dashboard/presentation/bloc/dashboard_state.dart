part of 'dashboard_bloc.dart';

abstract class DashboardState extends Equatable {
  const DashboardState();
  
  @override
  List<Object> get props => [];
}

class DashboardInitial extends DashboardState {}

class DashboardLoading extends DashboardState {}

class DashboardLoaded extends DashboardState {
  final VehicleState vehicleState;

  const DashboardLoaded({required this.vehicleState});

  @override
  List<Object> get props => [vehicleState];
}

class DashboardError extends DashboardState {
  final String message;

  const DashboardError({required this.message});

  @override
  List<Object> get props => [message];
}