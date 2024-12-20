import '../../domain/models/workshop.dart';
import '../../domain/repositories/workshop_repository.dart';

class MockWorkshopRepository implements WorkshopRepository {
  final List<Workshop> _workshops = [
    Workshop(
      id: '1',
      title: 'Introduction to Hand Building',
      description: 'Learn the basic techniques of hand building with clay. Perfect for beginners!',
      date: DateTime.now().add(const Duration(days: 7)),
      duration: 180, // 3 hours
      price: 89.99,
      skillLevel: 'Beginner',
      maxParticipants: 10,
      currentParticipants: 4,
      materialsIncluded: ['Clay', 'Basic tools', 'Glazes'],
      requirements: ['Apron', 'Enthusiasm to learn'],
      instructorName: 'Sarah Johnson',
      imageUrl: 'assets/images/workshop1.jpg',
    ),
    Workshop(
      id: '2',
      title: 'Wheel Throwing Basics',
      description: 'Get your hands dirty and learn the fundamentals of wheel throwing.',
      date: DateTime.now().add(const Duration(days: 14)),
      duration: 240, // 4 hours
      price: 129.99,
      skillLevel: 'Beginner',
      maxParticipants: 8,
      currentParticipants: 6,
      materialsIncluded: ['Clay', 'Tools', 'Glazes', 'Apron'],
      requirements: ['Close-toed shoes', 'Hair tie for long hair'],
      instructorName: 'Michael Chen',
      imageUrl: 'assets/images/workshop2.jpg',
    ),
    Workshop(
      id: '3',
      title: 'Advanced Glazing Techniques',
      description: 'Explore advanced glazing techniques and create unique finishes.',
      date: DateTime.now().add(const Duration(days: 21)),
      duration: 300, // 5 hours
      price: 159.99,
      skillLevel: 'Advanced',
      maxParticipants: 6,
      currentParticipants: 2,
      materialsIncluded: ['Multiple glazes', 'Test tiles', 'Advanced tools'],
      requirements: ['Previous pottery experience', 'Own pieces to glaze'],
      instructorName: 'Emma Thompson',
      imageUrl: 'assets/images/workshop3.jpg',
    ),
  ];

  @override
  Future<List<Workshop>> getWorkshops() async {
    await Future.delayed(const Duration(milliseconds: 800));
    return _workshops;
  }

  @override
  Future<Workshop> getWorkshopById(String id) async {
    await Future.delayed(const Duration(milliseconds: 500));
    return _workshops.firstWhere(
      (workshop) => workshop.id == id,
      orElse: () => throw Exception('Workshop not found'),
    );
  }

  @override
  Future<List<Workshop>> getUpcomingWorkshops() async {
    await Future.delayed(const Duration(milliseconds: 800));
    final now = DateTime.now();
    return _workshops.where((workshop) => workshop.date.isAfter(now)).toList();
  }

  @override
  Future<bool> registerForWorkshop(String workshopId, String userId) async {
    await Future.delayed(const Duration(milliseconds: 1000));
    final workshopIndex = _workshops.indexWhere((w) => w.id == workshopId);
    
    if (workshopIndex == -1) {
      throw Exception('Workshop not found');
    }

    final workshop = _workshops[workshopIndex];
    if (workshop.currentParticipants >= workshop.maxParticipants) {
      return false;
    }

    final updatedWorkshop = Workshop(
      id: workshop.id,
      title: workshop.title,
      description: workshop.description,
      date: workshop.date,
      duration: workshop.duration,
      price: workshop.price,
      skillLevel: workshop.skillLevel,
      maxParticipants: workshop.maxParticipants,
      currentParticipants: workshop.currentParticipants + 1,
      materialsIncluded: workshop.materialsIncluded,
      requirements: workshop.requirements,
      instructorName: workshop.instructorName,
      imageUrl: workshop.imageUrl,
    );

    _workshops[workshopIndex] = updatedWorkshop;
    return true;
  }

  @override
  Future<bool> cancelRegistration(String workshopId, String userId) async {
    await Future.delayed(const Duration(milliseconds: 1000));
    final workshopIndex = _workshops.indexWhere((w) => w.id == workshopId);
    
    if (workshopIndex == -1) {
      throw Exception('Workshop not found');
    }

    final workshop = _workshops[workshopIndex];
    if (workshop.currentParticipants <= 0) {
      return false;
    }

    final updatedWorkshop = Workshop(
      id: workshop.id,
      title: workshop.title,
      description: workshop.description,
      date: workshop.date,
      duration: workshop.duration,
      price: workshop.price,
      skillLevel: workshop.skillLevel,
      maxParticipants: workshop.maxParticipants,
      currentParticipants: workshop.currentParticipants - 1,
      materialsIncluded: workshop.materialsIncluded,
      requirements: workshop.requirements,
      instructorName: workshop.instructorName,
      imageUrl: workshop.imageUrl,
    );

    _workshops[workshopIndex] = updatedWorkshop;
    return true;
  }

  @override
  Future<List<Workshop>> getWorkshopsBySkillLevel(SkillLevel skillLevel) async {
    await Future.delayed(const Duration(milliseconds: 800));
    return _workshops.where((w) => w.skillLevel == skillLevel.displayName).toList();
  }
}
