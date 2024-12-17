import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../entities/vehicle_state.dart';

abstract class VehicleRepository {
  Future<Either<Failure, VehicleState>> getVehicleState();
  Future<Either<Failure, VehicleState>> updateVehicleState(VehicleState state);
  Stream<Either<Failure, VehicleState>> vehicleStateStream();
}