import 'package:desktop_app/screens/banner/banner_screen.dart';
import 'package:desktop_app/screens/dashboard/dashboard_screen.dart';
import 'package:desktop_app/screens/items/item_screen.dart';
import 'package:desktop_app/screens/settings/settings_screen.dart';
import 'package:flutter/material.dart';

void main() => runApp(const DesktopApp());

class DesktopApp extends StatelessWidget {
  const DesktopApp({super.key});
  
  @override
  Widget build(BuildContext context) => MaterialApp(
    title: 'Honkai: Starrail Warptracker',
    home: const DashboardScreen(),
    theme: ThemeData(
      primarySwatch: Colors.blue
    ),
    routes: {
      '/dashboard': (context) => const DashboardScreen(),
      '/items': (context) => const ItemScreen(),
      '/banner': (context) => const BannerScreen(),
      '/settings': (context) => const SettingsScreen(),
    },
  );
}