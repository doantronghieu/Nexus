import 'package:equatable/equatable.dart';

class VehicleState extends Equatable {
  final bool engineOn;
  final bool doorsLocked;
  final double temperature;
  final double speed;
  final double fuelLevel;
  final bool climateControlOn;
  final double climateTemp;
  final double batteryLevel;

  const VehicleState({
    this.engineOn = false,
    this.doorsLocked = true,
    this.temperature = 20.0,
    this.speed = 0.0,
    this.fuelLevel = 100.0,
    this.climateControlOn = false,
    this.climateTemp = 22.0,
    this.batteryLevel = 100.0,
  });

  VehicleState copyWith({
    bool? engineOn,
    bool? doorsLocked,
    double? temperature,
    double? speed,
    double? fuelLevel,
    bool? climateControlOn,
    double? climateTemp,
    double? batteryLevel,
  }) {
    return VehicleState(
      engineOn: engineOn ?? this.engineOn,
      doorsLocked: doorsLocked ?? this.doorsLocked,
      temperature: temperature ?? this.temperature,
      speed: speed ?? this.speed,
      fuelLevel: fuelLevel ?? this.fuelLevel,
      climateControlOn: climateControlOn ?? this.climateControlOn,
      climateTemp: climateTemp ?? this.climateTemp,
      batteryLevel: batteryLevel ?? this.batteryLevel,
    );
  }

  @override
  List<Object?> get props => [
        engineOn,
        doorsLocked,
        temperature,
        speed,
        fuelLevel,
        climateControlOn,
        climateTemp,
        batteryLevel,
      ];
}