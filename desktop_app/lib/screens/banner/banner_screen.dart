import 'package:desktop_app/screens/banner/grid_view.dart';
import 'package:desktop_app/screens/widgets/drawer.dart';
import 'package:flutter/material.dart';

class BannerScreen extends StatelessWidget {
  const BannerScreen({super.key});
  
  @override
  Widget build(BuildContext context) => _bannerScaffold();

  Scaffold _bannerScaffold() => Scaffold(
    appBar: AppBar(
      title: const Text('Banner'),
      centerTitle: true,
    ),
    body: BannerGridView(),
    drawer: const SideDrawer(),
  );
}