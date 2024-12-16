class VehicleState {
  final bool engineOn;
  final bool doorsLocked;
  final double temperature;
  final double speed;
  final double fuelLevel;
  final bool climateControlOn;
  final double climateTemp;
  final double batteryLevel;

  VehicleState({
    this.engineOn = false,
    this.doorsLocked = true,
    this.temperature = 20.0,
    this.speed = 0.0,
    this.fuelLevel = 100.0,
    this.climateControlOn = false,
    this.climateTemp = 22.0,
    this.batteryLevel = 100.0,
  });

  factory VehicleState.fromJson(Map<String, dynamic> json) {
    return VehicleState(
      engineOn: json['engineOn'] ?? false,
      doorsLocked: json['doorsLocked'] ?? true,
      temperature: json['temperature']?.toDouble() ?? 20.0,
      speed: json['speed']?.toDouble() ?? 0.0,
      fuelLevel: json['fuelLevel']?.toDouble() ?? 100.0,
      climateControlOn: json['climateControlOn'] ?? false,
      climateTemp: json['climateTemp']?.toDouble() ?? 22.0,
      batteryLevel: json['batteryLevel']?.toDouble() ?? 100.0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'engineOn': engineOn,
      'doorsLocked': doorsLocked,
      'temperature': temperature,
      'speed': speed,
      'fuelLevel': fuelLevel,
      'climateControlOn': climateControlOn,
      'climateTemp': climateTemp,
      'batteryLevel': batteryLevel,
    };
  }

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
}
