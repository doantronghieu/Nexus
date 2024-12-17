import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../entities/vehicle_state.dart';
import '../repositories/vehicle_repository.dart';

class UpdateVehicleState {
  final VehicleRepository repository;

  UpdateVehicleState(this.repository);

  Future<Either<Failure, VehicleState>> call(VehicleState state) async {
    return await repository.updateVehicleState(state);
  }
}