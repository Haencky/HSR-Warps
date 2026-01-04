import 'package:desktop_app/screens/dashboard/dashboard_screen.dart';
import 'package:flutter/material.dart';

void main() => runApp(const DesktopApp());

class DesktopApp extends StatelessWidget {
  const DesktopApp({super.key});
  
  @override
  Widget build(BuildContext context) => MaterialApp(
    title: 'Honkai: Starrail Warptracker',
    home: indexScaffold()
  );

}