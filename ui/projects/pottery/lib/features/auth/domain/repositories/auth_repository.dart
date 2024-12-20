import '../models/user.dart';

abstract class AuthRepository {
  Future<User> signIn(String email, String password);
  Future<User> signUp(String email, String password, String name);
  Future<void> signOut();
  Future<void> resetPassword(String email);
  Future<User?> getCurrentUser();
  Future<User> updateUser(User user);
  Future<void> updatePassword(String oldPassword, String newPassword);
  Stream<User?> get authStateChanges;
}
