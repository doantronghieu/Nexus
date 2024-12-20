import 'dart:async';
import '../../domain/models/user.dart';
import '../../domain/repositories/auth_repository.dart';

class MockAuthRepository implements AuthRepository {
  User? _currentUser;
  final _authStateController = StreamController<User?>.broadcast();

  @override
  Stream<User?> get authStateChanges => _authStateController.stream;

  @override
  Future<User> signIn(String email, String password) async {
    // Simulate network delay
    await Future.delayed(const Duration(milliseconds: 1500));
    
    // Simulate basic validation
    if (email.isEmpty || password.isEmpty) {
      throw Exception('Email and password cannot be empty');
    }

    if (password.length < 6) {
      throw Exception('Password must be at least 6 characters');
    }

    // Create a mock user
    _currentUser = User(
      id: 'user123',
      email: email,
      name: 'John Doe',
      phoneNumber: '+1234567890',
      profileImageUrl: 'assets/images/default_profile.jpg',
      workshopRegistrations: ['workshop1', 'workshop2'],
      orderHistory: ['order1', 'order2'],
      address: Address(
        street: '123 Main St',
        city: 'Springfield',
        state: 'IL',
        zipCode: '62701',
        country: 'USA',
      ),
    );

    _authStateController.add(_currentUser);
    return _currentUser!;
  }

  @override
  Future<User> signUp(String email, String password, String name) async {
    // Simulate network delay
    await Future.delayed(const Duration(milliseconds: 1500));
    
    // Simulate basic validation
    if (email.isEmpty || password.isEmpty || name.isEmpty) {
      throw Exception('All fields are required');
    }

    if (password.length < 6) {
      throw Exception('Password must be at least 6 characters');
    }

    // Create a new user
    _currentUser = User(
      id: 'user${DateTime.now().millisecondsSinceEpoch}',
      email: email,
      name: name,
    );

    _authStateController.add(_currentUser);
    return _currentUser!;
  }

  @override
  Future<void> signOut() async {
    await Future.delayed(const Duration(milliseconds: 500));
    _currentUser = null;
    _authStateController.add(null);
  }

  @override
  Future<void> resetPassword(String email) async {
    await Future.delayed(const Duration(milliseconds: 1000));
    if (email.isEmpty) {
      throw Exception('Email cannot be empty');
    }
    // Simulate sending password reset email
  }

  @override
  Future<User?> getCurrentUser() async {
    await Future.delayed(const Duration(milliseconds: 500));
    return _currentUser;
  }

  @override
  Future<User> updateUser(User user) async {
    await Future.delayed(const Duration(milliseconds: 1000));
    _currentUser = user;
    _authStateController.add(_currentUser);
    return user;
  }

  @override
  Future<void> updatePassword(String oldPassword, String newPassword) async {
    await Future.delayed(const Duration(milliseconds: 1000));
    
    if (oldPassword.isEmpty || newPassword.isEmpty) {
      throw Exception('Passwords cannot be empty');
    }

    if (newPassword.length < 6) {
      throw Exception('New password must be at least 6 characters');
    }

    // Simulate password update
  }

  void dispose() {
    _authStateController.close();
  }
}
