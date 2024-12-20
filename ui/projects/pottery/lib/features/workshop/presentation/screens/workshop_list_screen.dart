import 'package:flutter/material.dart';
import '../../data/repositories/mock_workshop_repository.dart';
import '../../domain/models/workshop.dart';
import '../widgets/workshop_card.dart';

class WorkshopListScreen extends StatefulWidget {
  const WorkshopListScreen({super.key});

  @override
  State<WorkshopListScreen> createState() => _WorkshopListScreenState();
}

class _WorkshopListScreenState extends State<WorkshopListScreen> {
  final _repository = MockWorkshopRepository();
  List<Workshop> _workshops = [];
  bool _isLoading = true;
  String? _selectedSkillLevel;

  @override
  void initState() {
    super.initState();
    _loadWorkshops();
  }

  Future<void> _loadWorkshops() async {
    setState(() => _isLoading = true);
    try {
      final workshops = await _repository.getUpcomingWorkshops();
      setState(() {
        _workshops = workshops;
        _isLoading = false;
      });
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error loading workshops: ${e.toString()}')),
        );
      }
      setState(() => _isLoading = false);
    }
  }

  Future<void> _filterBySkillLevel(SkillLevel? skillLevel) async {
    if (skillLevel == null) {
      await _loadWorkshops();
      return;
    }

    setState(() => _isLoading = true);
    try {
      final workshops = await _repository.getWorkshopsBySkillLevel(skillLevel);
      setState(() {
        _workshops = workshops;
        _selectedSkillLevel = skillLevel.displayName;
        _isLoading = false;
      });
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error filtering workshops: ${e.toString()}')),
        );
      }
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Pottery Workshops'),
        centerTitle: true,
      ),
      body: Column(
        children: [
          // Skill level filter
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: [
                  FilterChip(
                    label: const Text('All'),
                    selected: _selectedSkillLevel == null,
                    onSelected: (_) {
                      setState(() => _selectedSkillLevel = null);
                      _loadWorkshops();
                    },
                  ),
                  const SizedBox(width: 8),
                  ...SkillLevel.values.map(
                    (level) => Padding(
                      padding: const EdgeInsets.only(right: 8.0),
                      child: FilterChip(
                        label: Text(level.displayName),
                        selected: _selectedSkillLevel == level.displayName,
                        onSelected: (_) => _filterBySkillLevel(level),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          
          // Workshop list
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : _workshops.isEmpty
                    ? Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            const Icon(
                              Icons.event_busy,
                              size: 64,
                              color: Colors.grey,
                            ),
                            const SizedBox(height: 16),
                            Text(
                              'No workshops available',
                              style: Theme.of(context).textTheme.titleLarge,
                            ),
                            if (_selectedSkillLevel != null) ...[
                              const SizedBox(height: 8),
                              TextButton(
                                onPressed: _loadWorkshops,
                                child: const Text('Show all workshops'),
                              ),
                            ],
                          ],
                        ),
                      )
                    : ListView.builder(
                        padding: const EdgeInsets.all(16.0),
                        itemCount: _workshops.length,
                        itemBuilder: (context, index) {
                          final workshop = _workshops[index];
                          return Padding(
                            padding: const EdgeInsets.only(bottom: 16.0),
                            child: WorkshopCard(workshop: workshop),
                          );
                        },
                      ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _loadWorkshops,
        label: const Text('Refresh'),
        icon: const Icon(Icons.refresh),
      ),
    );
  }
}
