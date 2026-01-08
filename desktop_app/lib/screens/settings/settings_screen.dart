import 'package:desktop_app/screens/settings/listview.dart';
import 'package:desktop_app/screens/widgets/drawer.dart';
import 'package:flutter/material.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) => _settingsScaffold();
  

  Scaffold _settingsScaffold() => Scaffold(
    appBar: AppBar(
      title: const Text('Settings'),
      centerTitle: true,
    ),
    body: SettingsBody(),
    drawer: const SideDrawer(),
  );
}