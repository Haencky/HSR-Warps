import 'package:desktop_app/screens/dashboard/grid_view.dart';
import 'package:desktop_app/screens/widgets/main_scaffold.dart';
import 'package:flutter/material.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) => MainScaffold(
    titleText: 'Honkai Starrail Warptracker',
    contentBody: indexGridView(),
  );
}
