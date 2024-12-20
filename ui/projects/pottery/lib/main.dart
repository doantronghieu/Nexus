import 'package:flutter/material.dart';
import 'core/providers/app_state.dart';
import 'features/auth/data/repositories/mock_auth_repository.dart';
import 'features/auth/domain/models/user.dart';
import 'features/auth/presentation/screens/sign_in_screen.dart';
import 'features/product_catalog/presentation/screens/product_list_screen.dart';
import 'features/workshop/presentation/screens/workshop_list_screen.dart';
import 'features/auth/presentation/screens/profile_screen.dart';

void main() {
  runApp(const PotteryApp());
}

class PotteryApp extends StatelessWidget {
  const PotteryApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const AppStateProvider(
      child: MaterialApp(
        title: 'Pottery Store',
        home: AuthWrapper(),
      ),
    );
  }
}

class AuthWrapper extends StatefulWidget {
  const AuthWrapper({super.key});

  @override
  State<AuthWrapper> createState() => _AuthWrapperState();
}

class _AuthWrapperState extends State<AuthWrapper> {
  final _authRepository = MockAuthRepository();
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _checkCurrentUser();
  }

  Future<void> _checkCurrentUser() async {
    try {
      final user = await _authRepository.getCurrentUser();
      if (mounted) {
        final appState = AppState.of(context);
        appState?.updateUser(user);
        setState(() => _loading = false);
      }
    } catch (e) {
      if (mounted) {
        setState(() => _loading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Scaffold(
        body: Center(
          child: CircularProgressIndicator(),
        ),
      );
    }

    final appState = AppState.of(context);
    final User? currentUser = appState?.currentUser;

    if (currentUser == null) {
      return const SignInScreen();
    }

    return MainScreen(user: currentUser);
  }
}

class MainScreen extends StatefulWidget {
  final User user;

  const MainScreen({
    super.key,
    required this.user,
  });

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _selectedIndex,
        children: [
          const ProductListScreen(),
          const WorkshopListScreen(),
          ProfileScreen(user: widget.user),
        ],
      ),
      bottomNavigationBar: NavigationBar(
        onDestinationSelected: (index) {
          setState(() => _selectedIndex = index);
        },
        selectedIndex: _selectedIndex,
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.store),
            label: 'Shop',
          ),
          NavigationDestination(
            icon: Icon(Icons.event),
            label: 'Workshops',
          ),
          NavigationDestination(
            icon: Icon(Icons.person),
            label: 'Profile',
          ),
        ],
      ),
    );
  }
}
