import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:equatable/equatable.dart';
import '../../domain/entities/vehicle_state.dart';
import '../../domain/usecases/get_vehicle_state.dart';
import '../../domain/usecases/update_vehicle_state.dart';

part 'dashboard_event.dart';
part 'dashboard_state.dart';

class DashboardBloc extends Bloc<DashboardEvent, DashboardState> {
  final GetVehicleState getVehicleState;
  final UpdateVehicleState updateVehicleState;

  DashboardBloc({
    required this.getVehicleState,
    required this.updateVehicleState,
  }) : super(DashboardInitial()) {
    on<GetVehicleStateEvent>(_onGetVehicleState);
    on<UpdateVehicleStateEvent>(_onUpdateVehicleState);
  }

  Future<void> _onGetVehicleState(
    GetVehicleStateEvent event,
    Emitter<DashboardState> emit,
  ) async {
    emit(DashboardLoading());
    final result = await getVehicleState();
    result.fold(
      (failure) => emit(DashboardError(message: failure.message)),
      (vehicleState) => emit(DashboardLoaded(vehicleState: vehicleState)),
    );
  }

  Future<void> _onUpdateVehicleState(
    UpdateVehicleStateEvent event,
    Emitter<DashboardState> emit,
  ) async {
    final result = await updateVehicleState(event.vehicleState);
    result.fold(
      (failure) => emit(DashboardError(message: failure.message)),
      (vehicleState) => emit(DashboardLoaded(vehicleState: vehicleState)),
    );
  }
}