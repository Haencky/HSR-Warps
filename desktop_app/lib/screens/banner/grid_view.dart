import 'dart:convert';
import 'package:desktop_app/services/api_service.dart';
import 'package:desktop_app/services/settings_service.dart';
import 'package:flutter/material.dart';

class BannerGridView extends StatefulWidget {
  const BannerGridView({super.key});

  @override
  State<BannerGridView> createState() => _BannerGridViewState();
}

class _BannerGridViewState extends State<BannerGridView> {
  List<dynamic> allBanners = [];
  List<dynamic> displayedBanners = [];
  List<dynamic> itemTypes = [];
  String? activeFilter;
  bool isLoading = true;
  String url = '';
  String port = '';
  
  final double sizeStackDescription = 20;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    try {
      List<dynamic> response = await Future.wait([
        ApiService.fetchApi('api/banners'),
        ApiService.fetchApi('api/item_types'),
        SettingsService.getSettings()
      ]);
      if (response[0].statusCode == 200 && response[1].statusCode == 200) {
        setState(() {
          allBanners = jsonDecode(response[0].body).where((b) => b['hsr_gacha_id'] != 1001).toList();
          allBanners.sort((a, b) => (b['hsr_gacha_id'] % 1000).compareTo(a['hsr_gacha_id'] % 1000));
          itemTypes = jsonDecode(response[1].body);
          displayedBanners = List.from(allBanners);
          isLoading = false;
          var settings = response[2];
          url = settings['url'];
          port = settings['port'];
        });
      }
    } catch (e) {
      setState(() { isLoading = false; });
    }
  }

  void _sortByCount() {
    setState(() {
      displayedBanners.sort((a, b) => b['count'].compareTo(a['count']));
    });
  }

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
              FilterChip(
                label: const Text('All'),
                selected: activeFilter == null,
                onSelected:(_) => setState(() {
                  activeFilter = null;
                  displayedBanners = List.from(allBanners);
                }),
              ),
              for (var type in itemTypes)
                FilterChip(
                  label: Text(type['name']),
                  selected: activeFilter == type['name'],
                  onSelected: (selected) => setState(() {
                      activeFilter = selected ? type['name'] : null;
                      if (activeFilter != null) {
                        displayedBanners = allBanners.where((b) => b['item_type'] == type['name']).toList();
                      } else {
                        displayedBanners = List.from(allBanners);
                      }
                  })
                ),
              ActionChip(
                avatar: const Icon(Icons.sort),
                label: const Text('Pulls'), 
                onPressed: _sortByCount
              ),
            ],
          ),
        ),
        
        Expanded(
          child: Container(
            padding: const EdgeInsets.all(20),
            child: GridView.count(
              crossAxisCount: 3,
              mainAxisSpacing: 10,
              crossAxisSpacing: 10,
              children: [
                for (var b in displayedBanners)
                  _buildBannerContainer(b)
              ],
            ),
          ),
        ),
      ],
    );
  }
  Widget _buildBannerContainer(dynamic b) => Container(
    padding: EdgeInsets.all(10),
    alignment: Alignment.center,
    decoration: BoxDecoration(
      borderRadius: BorderRadius.all(Radius.circular(50)),
      border: Border.all(
        width: 2.5,
        style: BorderStyle.solid,
        color: b['ff'] == 0 ? Colors.greenAccent : Colors.redAccent
      ),
    ),
    child: Stack(
      alignment: Alignment.topLeft,
      children: [
        Image.network(
          '$url:$port${b["item_image"]}',
          width: 770,
          height: 1000,
          errorBuilder: (context, object, stackTrace) => SizedBox(
            height: 1000,
            width: 770,
            child: Center(
              child: ListTile(
                title: Text('No item connected to banner', style: TextStyle(fontWeight: FontWeight.bold)),
                subtitle: b['hsr_gacha_id'].toString()[0] == '2' ? Text('Item in banner is a character') : Text('Item in banner is a light cone'),
                leading: Icon(Icons.question_mark),
              )
            )
          )
        ),
        Container(
          padding: EdgeInsets.fromLTRB(3, 3, 0, 0),
          //color: Colors.black87,
          child: Row(
            mainAxisSize: MainAxisSize.min,
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('${b['count']}\t',
                  style: TextStyle(
                  color: b['obtained'] == 5 ? Colors.green : Colors.red,
                  fontSize: sizeStackDescription
                ),
              ),
              Image.asset(
                'assets/images/ticket.png',
                //fit: BoxFit.scaleDown,
                height: (sizeStackDescription + 7),
                width: (sizeStackDescription + 7),
              )
            ]
          ),
        )
      ],
    ),
  );
}