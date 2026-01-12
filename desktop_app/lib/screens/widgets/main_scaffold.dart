import 'dart:convert';
import 'package:desktop_app/screens/widgets/drawer.dart';
import 'package:desktop_app/screens/widgets/item_list_tile.dart';
import 'package:desktop_app/services/api_service.dart';
import 'package:desktop_app/services/settings_service.dart';
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

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
      ApiService.fetchApi('api/items'),
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
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          showDialog(
            context: context,
            builder: (context) {
              String addedItem = '';
              String msg = '';
              bool isLoading = false;
              bool isSuccess = false;
              bool hasSuggestions = false;
              List<dynamic> suggestions = [];
              String changeUrl = '';

              return StatefulBuilder(
                builder: (context, setStateInside) {
                  if (isSuccess) {
                    return AlertDialog(
                      content: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Icon(Icons.check_circle, color: Colors.green, size: 60),
                          const SizedBox(height: 16),
                          Text('$msg; you should edit it by clicking the button below'),
                          IconButton(
                            onPressed: () async {
                              await launchUrl(Uri.parse(changeUrl));
                              Navigator.pop(context, true);
                            },
                            icon: const Icon(Icons.edit)
                          )
                        ],
                      ),
                    );
                  } if (hasSuggestions) {
                    return AlertDialog(
                      title: Text('$msg, try:'),
                      content: Column(
                          children: [
                            SizedBox(
                              height: 300,
                              width: double.maxFinite,
                              child: ListView.separated(
                                shrinkWrap: true,
                                itemBuilder: (context, i) => ListTile(
                                  title: Text(suggestions[i]),
                                  leading: Text('${i+1}'),
                                ),
                                separatorBuilder: (context, i) => const Divider(),
                                itemCount: suggestions.length
                              ),
                          ),
                          const SizedBox(height: 16),
                          TextButton(
                            onPressed: () => setStateInside(() {
                              hasSuggestions = false;
                              isLoading = false;
                            }),
                            child: Text('Ok')
                          )
                        ]
                      )
                    );
                  }
                  return AlertDialog(
                    title: const Text('Add a new item'),
                    content: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        TextField(
                          onChanged: (value) => setStateInside(() => addedItem = value),
                          focusNode: FocusNode(canRequestFocus: true),
                          decoration: const InputDecoration(
                            hintText: 'Enter english name',
                            border: OutlineInputBorder(),
                          ),
                        ),
                        isLoading
                          ? const CircularProgressIndicator()
                          :  TextButton(
                              onPressed: addedItem.isEmpty ? null : () async {
                                setStateInside(() => isLoading = true);
                                final List<dynamic> response = await Future.wait([
                                  ApiService.sendToApi('api/add', {'eng_name': addedItem}),
                                  ApiService.fetchItemIds(),
                                  SettingsService.getSettings()
                                ]);

                                setStateInside(() {
                                  isLoading = false;
                                  if (response[0].statusCode == 200 || response[0].statusCode == 201) {
                                    final Map<String, dynamic> allItemsWithIds = jsonDecode(response[1].body);
                                    final data = jsonDecode(response[0].body);
                                    final message = data['message'];
                                    final sug = data['suggestions'];
                                    final id = data['id'];
                                    final settings = response[2];
                                    final url = settings['url'];
                                    final port = settings['port']; 
                                    if (message.toString().startsWith('Added item')) {
                                      isSuccess = true;
                                      changeUrl = '$url:$port/admin/warps/item/$id/change/';
                                    } else {
                                      hasSuggestions = true;
                                      if (sug.toList().length != 0) {
                                        suggestions = sug;
                                      } else {
                                        suggestions = allItemsWithIds.keys.toList();
                                      }
                                    }
                                    msg = message.toString();
                                  }
                                });
                              },
                              child: Text('Add item!')
                            )
                      ]
                    )
                  );
                }
              );
            }
          );
        },
        tooltip: 'Add a new item manually',
        child: const Icon(Icons.add),
      ),
    );
  }
}