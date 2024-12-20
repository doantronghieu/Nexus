import 'package:flutter/material.dart';
import '../../../../core/providers/app_state.dart';
import '../../data/repositories/mock_product_repository.dart';
import '../../domain/models/product.dart';
import '../widgets/product_card.dart';
import 'cart_screen.dart';

class ProductListScreen extends StatefulWidget {
  const ProductListScreen({super.key});

  @override
  State<ProductListScreen> createState() => _ProductListScreenState();
}

class _ProductListScreenState extends State<ProductListScreen> {
  final _repository = MockProductRepository();
  String? _selectedCategory;
  List<Product> _products = [];
  List<String> _categories = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    setState(() => _isLoading = true);
    try {
      final categories = await _repository.getCategories();
      final products = await _repository.getProducts();
      setState(() {
        _categories = categories;
        _products = products;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error loading products: ${e.toString()}')),
        );
      }
    }
  }

  Future<void> _filterByCategory(String? category) async {
    setState(() {
      _isLoading = true;
      _selectedCategory = category;
    });

    try {
      final products = category == null 
          ? await _repository.getProducts()
          : await _repository.getProductsByCategory(category);
      setState(() {
        _products = products;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error filtering products: ${e.toString()}')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final cartItemCount = AppState.of(context)?.cartItems.length ?? 0;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Pottery Store'),
        centerTitle: true,
        actions: [
          Stack(
            children: [
              IconButton(
                icon: const Icon(Icons.shopping_cart),
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => const CartScreen(),
                    ),
                  );
                },
              ),
              if (cartItemCount > 0)
                Positioned(
                  right: 8,
                  top: 8,
                  child: Container(
                    padding: const EdgeInsets.all(2),
                    decoration: BoxDecoration(
                      color: Theme.of(context).colorScheme.error,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    constraints: const BoxConstraints(
                      minWidth: 16,
                      minHeight: 16,
                    ),
                    child: Text(
                      '$cartItemCount',
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 10,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ),
                ),
            ],
          ),
        ],
      ),
      body: Column(
        children: [
          // Category filter
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: [
                  FilterChip(
                    label: const Text('All'),
                    selected: _selectedCategory == null,
                    onSelected: (_) => _filterByCategory(null),
                  ),
                  const SizedBox(width: 8),
                  ..._categories.map(
                    (category) => Padding(
                      padding: const EdgeInsets.only(right: 8.0),
                      child: FilterChip(
                        label: Text(category),
                        selected: _selectedCategory == category,
                        onSelected: (_) => _filterByCategory(category),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          // Product grid
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : GridView.builder(
                    padding: const EdgeInsets.all(16.0),
                    gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 2,
                      childAspectRatio: 0.65,
                      crossAxisSpacing: 16.0,
                      mainAxisSpacing: 16.0,
                    ),
                    itemCount: _products.length,
                    itemBuilder: (context, index) {
                      final product = _products[index];
                      return ProductCard(product: product);
                    },
                  ),
          ),
        ],
      ),
    );
  }
}
