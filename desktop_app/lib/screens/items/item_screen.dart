import 'package:desktop_app/screens/items/item_body.dart';
import 'package:desktop_app/screens/widgets/main_scaffold.dart';
import 'package:flutter/material.dart';

class ItemScreen extends StatelessWidget {
  const ItemScreen({super.key});
  
  @override
  Widget build(BuildContext context) => MainScaffold(
    titleText: 'Items',
    contentBody: ItemBody(),
  );
}