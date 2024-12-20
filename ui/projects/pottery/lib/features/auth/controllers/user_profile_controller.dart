import 'package:flutter/foundation.dart';
import '../domain/models/user.dart';

class UserProfileController extends ChangeNotifier {
  static final UserProfileController _instance = UserProfileController._internal();
  factory UserProfileController() => _instance;
  UserProfileController._internal();

  User? _currentUser;
  User? get currentUser => _currentUser;
  bool get isAuthenticated => _currentUser != null;

  void setUser(User? user) {
    _currentUser = user;
    notifyListeners();
  }

  void updateUserProfile({
    String? name,
    String? phoneNumber,
    Address? address,
    String? profileImageAsset,
  }) {
    if (_currentUser == null) return;

    _currentUser = _currentUser!.copyWith(
      name: name,
      phoneNumber: phoneNumber,
      address: address,
      profileImageUrl: profileImageAsset,
    );
    notifyListeners();
  }

  void clearUser() {
    _currentUser = null;
    notifyListeners();
  }
}
