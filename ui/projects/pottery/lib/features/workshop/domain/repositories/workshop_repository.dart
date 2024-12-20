import '../models/workshop.dart';

abstract class WorkshopRepository {
  Future<List<Workshop>> getWorkshops();
  Future<Workshop> getWorkshopById(String id);
  Future<List<Workshop>> getUpcomingWorkshops();
  Future<bool> registerForWorkshop(String workshopId, String userId);
  Future<bool> cancelRegistration(String workshopId, String userId);
  Future<List<Workshop>> getWorkshopsBySkillLevel(SkillLevel skillLevel);
}
