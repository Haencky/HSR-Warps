import 'package:desktop_app/screens/banner/grid_view.dart';
import 'package:desktop_app/screens/widgets/main_scaffold.dart';
import 'package:flutter/material.dart';

class BannerScreen extends StatelessWidget {
  const BannerScreen({super.key});
  
  @override
  Widget build(BuildContext context) => MainScaffold(
    titleText: 'Banner',
    contentBody: BannerGridView()
  );
}