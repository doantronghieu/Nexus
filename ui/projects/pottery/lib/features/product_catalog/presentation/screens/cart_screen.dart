import 'package:flutter/material.dart';
import '../../../../core/providers/app_state.dart';
import '../../domain/models/product.dart';

class CartScreen extends StatelessWidget {
  const CartScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final appState = AppState.of(context);
    final cartItems = appState?.cartItems ?? [];
    
    if (cartItems.isEmpty) {
      return Scaffold(
        appBar: AppBar(
          title: const Text('Shopping Cart'),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                Icons.shopping_cart_outlined,
                size: 64,
                color: Colors.grey[400],
              ),
              const SizedBox(height: 16),
              Text(
                'Your cart is empty',
                style: Theme.of(context).textTheme.titleLarge,
              ),
              const SizedBox(height: 8),
              ElevatedButton(
                onPressed: () => Navigator.pop(context),
                child: const Text('Continue Shopping'),
              ),
            ],
          ),
        ),
      );
    }

    // Calculate totals
    final totalItems = cartItems.length;
    final subtotal = cartItems.fold<double>(
      0,
      (sum, item) => sum + item.price,
    );
    const shippingCost = 10.0; // Fixed shipping cost
    final total = subtotal + shippingCost;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Shopping Cart'),
        actions: [
          if (cartItems.isNotEmpty)
            IconButton(
              icon: const Icon(Icons.delete_outline),
              onPressed: () {
                showDialog(
                  context: context,
                  builder: (context) => AlertDialog(
                    title: const Text('Clear Cart'),
                    content: const Text(
                      'Are you sure you want to remove all items from your cart?',
                    ),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(context),
                        child: const Text('Cancel'),
                      ),
                      TextButton(
                        onPressed: () {
                          // Clear cart functionality will be added
                          Navigator.pop(context);
                        },
                        child: const Text('Clear'),
                      ),
                    ],
                  ),
                );
              },
            ),
        ],
      ),
      body: Column(
        children: [
          // Cart Items List
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: cartItems.length,
              itemBuilder: (context, index) {
                final product = cartItems[index];
                return CartItemCard(product: product);
              },
            ),
          ),

          // Order Summary
          Card(
            margin: EdgeInsets.zero,
            shape: const RoundedRectangleBorder(
              borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
            ),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: SafeArea(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    Text(
                      'Order Summary',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                    const SizedBox(height: 16),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          'Subtotal ($totalItems items)',
                          style: Theme.of(context).textTheme.bodyLarge,
                        ),
                        Text(
                          '\$${subtotal.toStringAsFixed(2)}',
                          style: Theme.of(context).textTheme.bodyLarge,
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          'Shipping',
                          style: Theme.of(context).textTheme.bodyLarge,
                        ),
                        Text(
                          '\$${shippingCost.toStringAsFixed(2)}',
                          style: Theme.of(context).textTheme.bodyLarge,
                        ),
                      ],
                    ),
                    const Divider(height: 24),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          'Total',
                          style: Theme.of(context).textTheme.titleLarge,
                        ),
                        Text(
                          '\$${total.toStringAsFixed(2)}',
                          style: Theme.of(context).textTheme.titleLarge?.copyWith(
                                color: Theme.of(context).primaryColor,
                              ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: () {
                        // Checkout functionality will be added
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text('Checkout functionality coming soon'),
                          ),
                        );
                      },
                      style: ElevatedButton.styleFrom(
                        padding: const EdgeInsets.all(16),
                        textStyle: const TextStyle(fontSize: 16),
                      ),
                      child: const Text('Proceed to Checkout'),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class CartItemCard extends StatelessWidget {
  final Product product;

  const CartItemCard({
    super.key,
    required this.product,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      child: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Product Image
            ClipRRect(
              borderRadius: BorderRadius.circular(8),
              child: Image.asset(
                product.imageUrl,
                width: 80,
                height: 80,
                fit: BoxFit.cover,
                errorBuilder: (context, error, stackTrace) => Container(
                  width: 80,
                  height: 80,
                  color: Colors.grey[200],
                  child: const Icon(Icons.image_not_supported),
                ),
              ),
            ),
            const SizedBox(width: 16),

            // Product Details
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    product.name,
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                  const SizedBox(height: 4),
                  Text(
                    '\$${product.price.toStringAsFixed(2)}',
                    style: Theme.of(context).textTheme.titleSmall?.copyWith(
                          color: Theme.of(context).primaryColor,
                        ),
                  ),
                ],
              ),
            ),

            // Remove Button
            IconButton(
              icon: const Icon(Icons.delete_outline),
              onPressed: () {
                final appState = AppState.of(context);
                appState?.removeFromCart(product);
                
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: const Text('Item removed from cart'),
                    action: SnackBarAction(
                      label: 'Undo',
                      onPressed: () => appState?.addToCart(product),
                    ),
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}
