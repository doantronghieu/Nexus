import 'package:flutter/material.dart';
import 'package:car/dashboard_item.dart';

class DashboardRow extends StatelessWidget {
  final IconData icon1;
  final String value1;
  final IconData icon2;
  final String value2;

  const DashboardRow({
    super.key,
    required this.icon1,
    required this.value1,
    required this.icon2,
    required this.value2,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceAround,
      children: [
        DashboardItem(icon: icon1, value: value1),
        DashboardItem(icon: icon2, value: value2),
      ],
    );
  }
}
