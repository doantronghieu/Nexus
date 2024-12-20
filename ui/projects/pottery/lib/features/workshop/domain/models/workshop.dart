class Workshop {
  final String id;
  final String title;
  final String description;
  final DateTime date;
  final int duration; // in minutes
  final double price;
  final String skillLevel;
  final int maxParticipants;
  final int currentParticipants;
  final List<String> materialsIncluded;
  final List<String> requirements;
  final String instructorName;
  final String imageUrl;

  Workshop({
    required this.id,
    required this.title,
    required this.description,
    required this.date,
    required this.duration,
    required this.price,
    required this.skillLevel,
    required this.maxParticipants,
    required this.currentParticipants,
    required this.materialsIncluded,
    required this.requirements,
    required this.instructorName,
    required this.imageUrl,
  });

  bool get isAvailable => currentParticipants < maxParticipants;
  int get spotsLeft => maxParticipants - currentParticipants;

  factory Workshop.fromJson(Map<String, dynamic> json) {
    return Workshop(
      id: json['id'] as String,
      title: json['title'] as String,
      description: json['description'] as String,
      date: DateTime.parse(json['date'] as String),
      duration: json['duration'] as int,
      price: (json['price'] as num).toDouble(),
      skillLevel: json['skillLevel'] as String,
      maxParticipants: json['maxParticipants'] as int,
      currentParticipants: json['currentParticipants'] as int,
      materialsIncluded: List<String>.from(json['materialsIncluded'] as List),
      requirements: List<String>.from(json['requirements'] as List),
      instructorName: json['instructorName'] as String,
      imageUrl: json['imageUrl'] as String,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'description': description,
      'date': date.toIso8601String(),
      'duration': duration,
      'price': price,
      'skillLevel': skillLevel,
      'maxParticipants': maxParticipants,
      'currentParticipants': currentParticipants,
      'materialsIncluded': materialsIncluded,
      'requirements': requirements,
      'instructorName': instructorName,
      'imageUrl': imageUrl,
    };
  }
}

enum SkillLevel {
  beginner,
  intermediate,
  advanced;

  String get displayName {
    switch (this) {
      case SkillLevel.beginner:
        return 'Beginner';
      case SkillLevel.intermediate:
        return 'Intermediate';
      case SkillLevel.advanced:
        return 'Advanced';
    }
  }
}
