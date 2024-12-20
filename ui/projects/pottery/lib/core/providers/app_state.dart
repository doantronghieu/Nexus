import 'package:flutter/material.dart';
import '../../features/auth/domain/models/user.dart';
import '../../features/product_catalog/domain/models/product.dart';

class AppState extends InheritedWidget {
  final User? currentUser;
  final List<Product> cartItems;
  final Map<String, List<String>> workshopRegistrations;
  final Function(Product) addToCart;
  final Function(Product) removeFromCart;
  final Function(User?) updateUser;
  final Function(String userId, String profileImage) updateProfileImage;
  final Function(String, String) registerForWorkshop;
  final Function(String, String) cancelWorkshopRegistration;

  const AppState({
    super.key,
    required super.child,
    required this.currentUser,
    required this.cartItems,
    required this.workshopRegistrations,
    required this.addToCart,
    required this.removeFromCart,
    required this.updateUser,
    required this.updateProfileImage,
    required this.registerForWorkshop,
    required this.cancelWorkshopRegistration,
  });

  static AppState? of(BuildContext context) {
    return context.dependOnInheritedWidgetOfExactType<AppState>();
  }

  @override
  bool updateShouldNotify(AppState oldWidget) {
    return currentUser != oldWidget.currentUser ||
        cartItems != oldWidget.cartItems ||
        workshopRegistrations != oldWidget.workshopRegistrations;
  }
}

class AppStateProvider extends StatefulWidget {
  final Widget child;

  const AppStateProvider({
    super.key,
    required this.child,
  });

  @override
  State<AppStateProvider> createState() => _AppStateProviderState();
}

class _AppStateProviderState extends State<AppStateProvider> {
  User? _currentUser;
  final List<Product> _cartItems = [];
  final Map<String, List<String>> _workshopRegistrations = {};

  void _addToCart(Product product) {
    setState(() {
      _cartItems.add(product);
    });
  }

  void _removeFromCart(Product product) {
    setState(() {
      _cartItems.removeWhere((item) => item.id == product.id);
    });
  }

  void _updateUser(User? user) {
    setState(() {
      _currentUser = user;
    });
  }

  void _updateProfileImage(String userId, String profileImage) {
    if (_currentUser?.id != userId) return;
    setState(() {
      _currentUser = _currentUser?.copyWith(
        profileImageUrl: profileImage,
      );
    });
  }

  void _registerForWorkshop(String workshopId, String userId) {
    setState(() {
      _workshopRegistrations.putIfAbsent(workshopId, () => []).add(userId);
    });
  }

  void _cancelWorkshopRegistration(String workshopId, String userId) {
    setState(() {
      _workshopRegistrations[workshopId]?.remove(userId);
    });
  }

  @override
  Widget build(BuildContext context) {
    return AppState(
      currentUser: _currentUser,
      cartItems: _cartItems,
      workshopRegistrations: _workshopRegistrations,
      addToCart: _addToCart,
      removeFromCart: _removeFromCart,
      updateUser: _updateUser,
      updateProfileImage: _updateProfileImage,
      registerForWorkshop: _registerForWorkshop,
      cancelWorkshopRegistration: _cancelWorkshopRegistration,
      child: widget.child,
    );
  }
}
