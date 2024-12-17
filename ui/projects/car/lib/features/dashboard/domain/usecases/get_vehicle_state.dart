import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../entities/vehicle_state.dart';
import '../repositories/vehicle_repository.dart';

class GetVehicleState {
  final VehicleRepository repository;

  GetVehicleState(this.repository);

  Future<Either<Failure, VehicleState>> call() async {
    return await repository.getVehicleState();
  }
}