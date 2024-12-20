import 'package:flutter/foundation.dart';
import '../../features/auth/domain/models/user.dart';

class AuthService extends ChangeNotifier {
  User? _currentUser;
  
  User? get currentUser => _currentUser;
  
  bool get isAuthenticated => _currentUser != null;

  void setUser(User? user) {
    _currentUser = user;
    notifyListeners();
  }

  String get userId {
    if (_currentUser == null) {
      throw Exception('No authenticated user');
    }
    return _currentUser!.id;
  }
}
