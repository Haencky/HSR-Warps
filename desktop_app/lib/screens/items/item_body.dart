import 'dart:convert';

import 'package:desktop_app/services/api_service.dart';
import 'package:desktop_app/services/settings_service.dart';
import 'package:flutter/material.dart';

class ItemBody extends StatefulWidget {
  const ItemBody({super.key});
  
  @override
  State<ItemBody> createState() => _ItemBodyState();

}

class _ItemBodyState extends State<ItemBody> {

  List<dynamic> allItems = [];
  List<dynamic> displayedItems = [];
  List<dynamic> itemTypes = [];
  String? activeFilter;
  bool isLoading = true;
  Set<int> selectedRarities = {3,4,5};
  Map<int, dynamic> colors = {
    3: Colors.lightBlue.withValues(alpha: 0.3),
    4: Colors.deepPurple.withValues(alpha: 0.3),
    5: Colors.amber.withValues(alpha: 0.3)
  };

  Map<int, dynamic> colorsBorder = {
    3: Colors.lightBlue,
    4: Colors.deepPurple,
    5: Colors.amber
  };
  String url = '';
  String port = '';

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    try {
      List<dynamic> response = await Future.wait([
        ApiService.fetchApi('item_warps'),
        ApiService.fetchApi('item_types'),
        SettingsService.getSettings()
      ]);
      if (response[0].statusCode == 200 && response[1].statusCode == 200) {
        setState(() {
          allItems = jsonDecode(response[0].body);
          itemTypes = jsonDecode(response[1].body);
          displayedItems = List.from(allItems);
          isLoading = false;
          var settings = response[2];
          url = settings['url'];
          port = settings['port'];
        });
      }
    } catch (e) {
      setState(() => isLoading = false);
    }
  }

  void _sortByCount() => setState(() {
      displayedItems.sort((a, b) => b['count'].compareTo(a['count']));
  });

  void _sortByRarity() => setState(() {
      displayedItems.sort((a, b) => b['item_rarity'].compareTo(a['item_rarity']));
  });

  @override
  Widget build(BuildContext context) {
    if (isLoading) return const Center(child: CircularProgressIndicator());

    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(10),
          child: Wrap(
            spacing: 10,
            children: [
              for (var r in [3,4,5])
                FilterChip(
                  label: Text('$r ⭐'),
                  selected: selectedRarities.contains(r),
                  selectedColor: colors[r],
                  checkmarkColor: Colors.amber,
                  onSelected: (bool selected) {
                    if (selected) {
                      setState(() {
                        selectedRarities.add(r);
                        displayedItems = allItems.where((i) => selectedRarities.contains(i['item_rarity']) && (i['item_type'] == activeFilter || activeFilter == null)).toList();
                      });
                    } else {
                      if (selectedRarities.length > 1) {
                        setState(() {
                          selectedRarities.remove(r);
                          displayedItems = allItems.where((i) => selectedRarities.contains(i['item_rarity']) && (i['item_type'] == activeFilter || activeFilter == null)).toList();
                        });
                      }
                    }
                  }
                ),
              for (var t in itemTypes)
                FilterChip(
                  label: Text(t['name']),
                  selected: activeFilter == t['name'],
                  onSelected: (bool selected) => setState(() {
                    activeFilter = selected ? t['name'] : null;
                    displayedItems = allItems.where((i) => (i['item_type'] == t['name'] || activeFilter == null) && selectedRarities.contains(i['item_rarity'])).toList();
                  }),
                ),
              ActionChip(
                label: const Text('Count'),
                avatar: const Icon(Icons.sort),
                onPressed: _sortByCount,
              ),
              ActionChip(
                label: const Text('Rarity'),
                avatar: const Icon(Icons.sort),
                onPressed: _sortByRarity,
              )
            ],
          )
        ),
        Expanded(
          child: Container(
            padding: const EdgeInsets.all(20),
            child: GridView.count(
              crossAxisCount: 3,
              mainAxisSpacing: 10,
              crossAxisSpacing: 10,
              children: [
                for (var i in displayedItems)
                  _buildItemContainer(i)
              ]
            ),
          ),
        )
      ],
    );
  }

  Widget _buildItemContainer(dynamic i) => Container(
    padding: EdgeInsets.all(10),
    alignment: Alignment.center,
    decoration: BoxDecoration(
      borderRadius: BorderRadius.all(Radius.circular(20)),
      border: Border.all(
        width: 2.5,
        color: colorsBorder[i['item_rarity']],
        style: BorderStyle.solid
      )
    ),
    child: Stack(
      alignment: Alignment.topLeft,
      children: [
        Image.network(
          '$url:$port${i['item_image']}',
          width: 770,
          height: 1500,
        ),
        Container(
          padding: EdgeInsets.fromLTRB(3, 3, 0, 0),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('${i['count']}\t',
                  style: TextStyle(
                  color: Colors.black,
                  fontSize: 20
                ),
              ),
              Image.asset(
                'assets/images/ticket.png',
                //fit: BoxFit.scaleDown,
                height: 27,
                width: 27,
              )
            ],
          )
        )
      ],
    )
  );
}