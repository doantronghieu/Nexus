enum CarFeature {
  engine,
  doors,
  horn,
  climate,
  sunroof,
  headlights,
}

class CarState {
  final Map<CarFeature, bool> _featureStates = {};

  bool isFeatureActive(CarFeature feature) => _featureStates[feature] ?? false;

  void toggleFeature(CarFeature feature) {
    _featureStates[feature] = !isFeatureActive(feature);
  }
}
