import 'package:flutter/foundation.dart';
import '../../features/product_catalog/domain/models/product.dart';

class CartItem {
  final Product product;
  int quantity;

  CartItem({
    required this.product,
    this.quantity = 1,
  });
}

class CartService extends ChangeNotifier {
  final List<CartItem> _items = [];

  List<CartItem> get items => List.unmodifiable(_items);
  
  double get total => _items.fold(
        0,
        (sum, item) => sum + (item.product.price * item.quantity),
      );

  int get itemCount => _items.fold(
        0,
        (sum, item) => sum + item.quantity,
      );

  void addToCart(Product product) {
    final existingItem = _items.firstWhere(
      (item) => item.product.id == product.id,
      orElse: () => CartItem(product: product, quantity: 0),
    );

    if (existingItem.quantity == 0) {
      _items.add(existingItem);
    }

    existingItem.quantity++;
    notifyListeners();
  }

  void removeFromCart(Product product) {
    _items.removeWhere((item) => item.product.id == product.id);
    notifyListeners();
  }

  void updateQuantity(Product product, int quantity) {
    final item = _items.firstWhere(
      (item) => item.product.id == product.id,
      orElse: () => CartItem(product: product),
    );

    if (quantity <= 0) {
      _items.remove(item);
    } else {
      item.quantity = quantity;
    }
    
    notifyListeners();
  }

  void clearCart() {
    _items.clear();
    notifyListeners();
  }
}
