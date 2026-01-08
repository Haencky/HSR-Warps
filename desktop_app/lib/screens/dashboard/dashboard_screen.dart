import 'package:desktop_app/screens/dashboard/grid_view.dart';
import 'package:desktop_app/screens/widgets/drawer.dart';
import 'package:flutter/material.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) => _indexScaffold();

  Scaffold _indexScaffold() => Scaffold(
    appBar: AppBar(
      title: const Text('Honkai Starrail Warptracker'),
      centerTitle: true,
    ),
    body: indexGridView(),
    drawer: const SideDrawer(),
  );
}
