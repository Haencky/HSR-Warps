import 'package:desktop_app/screens/items/item_body.dart';
import 'package:desktop_app/screens/widgets/drawer.dart';
import 'package:flutter/material.dart';

class ItemScreen extends StatelessWidget {
  const ItemScreen({super.key});
  
  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(
      title: const Text('Items'),
      centerTitle: true,
    ),
    body: ItemBody(),
    drawer: const SideDrawer(),
  );
}