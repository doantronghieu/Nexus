import 'package:get_it/get_it.dart';
import '../../features/dashboard/data/repositories/vehicle_repository_impl.dart';
import '../../features/dashboard/domain/repositories/vehicle_repository.dart';
import '../../features/dashboard/domain/usecases/get_vehicle_state.dart';
import '../../features/dashboard/domain/usecases/update_vehicle_state.dart';
import '../../features/dashboard/presentation/bloc/dashboard_bloc.dart';

final sl = GetIt.instance;

Future<void> init() async {
  // Bloc
  sl.registerFactory(
    () => DashboardBloc(
      getVehicleState: sl(),
      updateVehicleState: sl(),
    ),
  );

  // Use cases
  sl.registerLazySingleton(() => GetVehicleState(sl()));
  sl.registerLazySingleton(() => UpdateVehicleState(sl()));

  // Repository
  sl.registerLazySingleton<VehicleRepository>(
    () => VehicleRepositoryImpl(),
  );
}