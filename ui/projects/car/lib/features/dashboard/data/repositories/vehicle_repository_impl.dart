import 'dart:async';
import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../../domain/entities/vehicle_state.dart';
import '../../domain/repositories/vehicle_repository.dart';

class VehicleRepositoryImpl implements VehicleRepository {
  final _vehicleStateController = StreamController<Either<Failure, VehicleState>>.broadcast();
  VehicleState _currentState = const VehicleState();

  @override
  Future<Either<Failure, VehicleState>> getVehicleState() async {
    try {
      return Right(_currentState);
    } catch (e) {
      return const Left(VehicleFailure(message: 'Failed to get vehicle state'));
    }
  }

  @override
  Future<Either<Failure, VehicleState>> updateVehicleState(VehicleState state) async {
    try {
      _currentState = state;
      _vehicleStateController.add(Right(state));
      return Right(state);
    } catch (e) {
      return const Left(VehicleFailure(message: 'Failed to update vehicle state'));
    }
  }

  @override
  Stream<Either<Failure, VehicleState>> vehicleStateStream() {
    return _vehicleStateController.stream;
  }
}