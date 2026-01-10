import 'dart:convert';

import 'package:desktop_app/screens/widgets/drawer.dart';
import 'package:desktop_app/screens/widgets/item_list_tile.dart';
import 'package:desktop_app/services/api_service.dart';
import 'package:desktop_app/services/settings_service.dart';
import 'package:flutter/material.dart';

class MainScaffold extends StatefulWidget {
  final String titleText;
  final Widget contentBody;

  const MainScaffold({
    super.key,
    required this.titleText,
    required this.contentBody
  });
  
  @override
  State<MainScaffold> createState() => _SearchItemState();

}

class _SearchItemState extends State<MainScaffold> {

  List<dynamic> allItems = [];
  final TextEditingController _searchController = TextEditingController();
  String searchQuery = '';
  String url = '';
  String port = '';

  @override
  void initState() {
    super.initState();
    _searchController.addListener(() {
      setState(() {
        searchQuery = _searchController.text.toLowerCase();
      });
    });
    _loadData();
  }

  Future<void> _loadData() async {
    List<dynamic> response = await Future.wait([
      ApiService.fetchApi('items'),
      SettingsService.getSettings()
    ]);
    if (response[0].statusCode == 200) {
      setState(() {
        allItems = jsonDecode(response[0].body);
        var settings = response[1];
        url = settings['url'];
        port = settings['port'];
      });
    } 
  }

  List<dynamic> _getFilteredItems() {
    if (searchQuery.isEmpty) {
      List<dynamic> items = allItems.toList();
      items.sort((a, b) => a['name'].compareTo(b['name']));
      return items;
    }
    List<dynamic> filtered = allItems.where((item) {
      final name = item['name'].toString().toLowerCase();
      final engName = item['eng_name'].toString().toLowerCase();
      return name.contains(searchQuery.toLowerCase()) || engName.contains(searchQuery.toLowerCase());
    }).toList();
    filtered.sort((a,b) => a['name'].compareTo(b['name']));
    return filtered;
  }

  ListView _buildSearchResults(List<dynamic> displayedItems) => ListView.separated(
    itemBuilder: (final ctx, int i) => ItemListTile(
      item: _getFilteredItems()[i],
      baseUrl: '$url:$port'
    ),
    separatorBuilder: (final ctx, final i) => const Divider(),
    itemCount: displayedItems.length
  ); 

  Widget _buildSearchBar() => Padding(
    padding: const EdgeInsets.all(10),
    child: TextField(
      controller: _searchController,
      onChanged: (value) => searchQuery = value,
      decoration: const InputDecoration(
        hintText: 'Search items...',
        border: OutlineInputBorder(),
        prefixIcon: Icon(Icons.search),
      ),
    ),
  );

  @override
  Widget build(BuildContext context) {
    final displayedItems = _getFilteredItems();

    return Scaffold(
      appBar: AppBar(
        title: Text(widget.titleText),
        centerTitle: true,
        actions: [
          if (searchQuery.isNotEmpty)
            IconButton(
              onPressed: () {
                _searchController.clear();
                setState(() => searchQuery = '');
              },
              icon: const Icon(Icons.clear)
            )
        ],
      ),
      body: Column(
        children: [
          _buildSearchBar(),
          Expanded(
            child: _searchController.text.isEmpty
            ? widget.contentBody // if no searchterm is given show content (banner or etc)
            : _buildSearchResults(displayedItems) // else show item results
          )
        ],
      ),
      drawer: SideDrawer(),
    );
  }
}