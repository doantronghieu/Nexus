part of 'dashboard_bloc.dart';

abstract class DashboardEvent extends Equatable {
  const DashboardEvent();

  @override
  List<Object> get props => [];
}

class GetVehicleStateEvent extends DashboardEvent {}

class UpdateVehicleStateEvent extends DashboardEvent {
  final VehicleState vehicleState;

  const UpdateVehicleStateEvent(this.vehicleState);

  @override
  List<Object> get props => [vehicleState];
}