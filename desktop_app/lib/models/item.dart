import 'package:desktop_app/services/api_service.dart' show ApiService;

class Item {
  final String typName;
  final String pathName;
  final String pathImageURL;
  final String imageURL;
  final int id;
  final String name;
  final String wiki;
  final int rarity;
  final String englishName;

  Item({
    required this.typName,
    required this.pathName,
    required this.pathImageURL,
    required this.imageURL,
    required this.id,
    required this.name,
    required this.wiki,
    required this.rarity,
    required this.englishName

  });

  factory Item.fromJson(Map<String, dynamic> json) => Item(
    id: json['item_id'],
    name: json['name'],
    typName: json['typ_name'],
    pathName: json['path_name'],
    pathImageURL: json['path_icon'],
    imageURL: ApiService.baseUrl + json['image_url'],
    wiki: json['wiki'],
    rarity: json['rarity'],
    englishName: json['eng_name']
  );
}