import 'dart:convert';
import 'dart:io';

import 'package:desktop_app/services/api_service.dart';
import 'package:desktop_app/services/url_service.dart';
import 'package:flutter/material.dart';

class SideDrawer extends StatelessWidget {
  const SideDrawer({super.key});
    
  @override
  Widget build(BuildContext context) => Drawer(
    child: ListView(
      children: [
        ListTile(
          title: const Text('Homepage'),
          leading: const Icon(Icons.home),
          onTap: () => Navigator.pushNamed(context, '/dashboard') ,
        ),
        Divider(),
        ListTile(
          title: const Text('Items'),
          leading: const Icon(Icons.card_giftcard),
          onTap: () => Navigator.pushNamed(context, '/items'),
        ),
        Divider(),
        ListTile(
          title: const Text('Banner'),
          leading: const Icon(Icons.flag),
          onTap: () => Navigator.pushNamed(context, '/banner'),
        ),
        Divider(),
        ListTile(
          title: const Text('Import'),
          leading: const Icon(Icons.input),
          onTap:  () async {
            showDialog(context: context,
              barrierDismissible: false,
              builder: (context) => const AlertDialog(
                content: Column(mainAxisSize: MainAxisSize.min, children: [CircularProgressIndicator(), SizedBox(height: 20,), Text('Loading')],),
              )
            );
            await _importAndShow(context);
          },
          enabled: Platform.isWindows,
        ),
        Divider(),
        ListTile(
          title: const Text('Settings'),
          leading: const Icon(Icons.settings),
          onTap: () => Navigator.pushNamed(context, '/settings'),
        ),
      ],
    )
  );

  static Future<void> _importAndShow(BuildContext context) async {
    String? url = await UrlService.getUrl();
    if(!context.mounted) return;
    String title;
    Widget content;

    if (url == null) {
      title = 'No gacha URL found';
      content = Text('Unabble to find Gacha URL on this device');
    } else if (url.startsWith('https://')) { // valid gacha url
      var response = await ApiService.sendToApi('api/add', {'url': url});
      Map<String, dynamic> data = jsonDecode(response.body);
      List<dynamic> details = data['details'];

      title = data['message'];
      content = Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Divider(),
          for (var i = 0; i < details.length; i++) ...[
            ListTile(
              title: Text(details[i].keys.first),
              trailing: Text(details[i].values.first.toString()),
            ),
            if (i < details.length -1) const Divider(),
          ]
        ]
      );
      Navigator.pop(context);
    } else {
      content = Text(url);
      title = 'No valid Gacha Log found';
    }

    showDialog(context: context,
    builder: (cnx) {
      return AlertDialog(
        content: content,
        title: Text(title),
        actions: [
          TextButton(onPressed: () { Navigator.pop(cnx); Navigator.pop(cnx); } , child: Icon(Icons.close))
        ],
      );
    });
  }
}