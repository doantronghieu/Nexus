import 'package:flutter/foundation.dart';
import '../domain/models/workshop.dart';

class WorkshopRegistration {
  final String workshopId;
  final String userId;
  final DateTime registrationDate;

  WorkshopRegistration({
    required this.workshopId,
    required this.userId,
    required this.registrationDate,
  });
}

class WorkshopController extends ChangeNotifier {
  static final WorkshopController _instance = WorkshopController._internal();
  factory WorkshopController() => _instance;
  WorkshopController._internal();

  final Map<String, List<String>> _registrations = {}; // workshopId -> List of userIds
  final List<WorkshopRegistration> _registrationHistory = [];

  bool isRegistered(String workshopId, String userId) {
    return _registrations[workshopId]?.contains(userId) ?? false;
  }

  List<String> getWorkshopRegistrations(String userId) {
    return _registrations.entries
        .where((entry) => entry.value.contains(userId))
        .map((entry) => entry.key)
        .toList();
  }

  Future<bool> registerForWorkshop(Workshop workshop, String userId) async {
    if (!workshop.isAvailable) return false;

    _registrations.putIfAbsent(workshop.id, () => []).add(userId);
    _registrationHistory.add(
      WorkshopRegistration(
        workshopId: workshop.id,
        userId: userId,
        registrationDate: DateTime.now(),
      ),
    );

    notifyListeners();
    return true;
  }

  Future<bool> cancelRegistration(String workshopId, String userId) async {
    final registrations = _registrations[workshopId];
    if (registrations == null) return false;

    final success = registrations.remove(userId);
    if (success) {
      notifyListeners();
    }
    return success;
  }

  List<WorkshopRegistration> getUserRegistrationHistory(String userId) {
    return _registrationHistory
        .where((reg) => reg.userId == userId)
        .toList();
  }
}
