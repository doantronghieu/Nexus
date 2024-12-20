import 'package:flutter_test/flutter_test.dart';
import 'package:pottery/main.dart';

void main() {
  testWidgets('App smoke test', (WidgetTester tester) async {
    await tester.pumpWidget(const PotteryApp());
    expect(find.text('Shop'), findsOneWidget);
    expect(find.text('Workshops'), findsOneWidget);
  });
}
