import 'package:desktop_app/screens/settings/listview.dart';
import 'package:desktop_app/screens/widgets/main_scaffold.dart';
import 'package:flutter/material.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) => MainScaffold(
    titleText: 'Settings',
    contentBody: SettingsBody()
  );
}