import '../../domain/models/product.dart';
import '../../domain/repositories/product_repository.dart';

class MockProductRepository implements ProductRepository {
  final List<Product> _products = [
    Product(
      id: '1',
      name: 'Ceramic Vase',
      description: 'Beautiful handcrafted ceramic vase with a unique glaze finish.',
      price: 89.99,
      imageUrl: 'assets/images/vase1.jpg',
      category: 'Vases',
      dimensions: {
        'height': '30cm',
        'width': '15cm',
        'depth': '15cm',
      },
      inStock: true,
    ),
    Product(
      id: '2',
      name: 'Decorative Bowl',
      description: 'Hand-thrown decorative bowl perfect for fruit or as a centerpiece.',
      price: 59.99,
      imageUrl: 'assets/images/bowl1.jpg',
      category: 'Bowls',
      dimensions: {
        'height': '10cm',
        'diameter': '25cm',
      },
      inStock: true,
    ),
    // Add more mock products here
  ];

  @override
  Future<List<Product>> getProducts() async {
    // Simulate network delay
    await Future.delayed(const Duration(milliseconds: 800));
    return _products;
  }

  @override
  Future<Product> getProductById(String id) async {
    await Future.delayed(const Duration(milliseconds: 500));
    return _products.firstWhere(
      (product) => product.id == id,
      orElse: () => throw Exception('Product not found'),
    );
  }

  @override
  Future<List<Product>> getProductsByCategory(String category) async {
    await Future.delayed(const Duration(milliseconds: 800));
    return _products.where((product) => product.category == category).toList();
  }

  @override
  Future<List<String>> getCategories() async {
    await Future.delayed(const Duration(milliseconds: 300));
    return _products.map((product) => product.category).toSet().toList();
  }
}
