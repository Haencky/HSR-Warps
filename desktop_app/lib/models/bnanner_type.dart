import 'package:desktop_app/models/item.dart';

class BannerType {
  final String name;
  final int pity;
  final bool warranted;
  final double? winrate;
  final int count;
  final Item? lastWin;
  final int maxPity;
  final int jade;
  final double euro;
  final int id;

  BannerType({
    required this.name,
    required this.pity,
    required this.warranted,
    this.winrate,
    required this.count,
    this.lastWin,
    required this.maxPity,
    required this.jade,
    required this.id,
    required this.euro
  });

  factory BannerType.fromJson(Map<String, dynamic> json) => BannerType(
    name: json['name'],
    pity: json['pity'],
    warranted: json['warranted'],
    winrate: json['wr'],
    count: json['c'],
    lastWin: Item.fromJson(json['last_win']),
    maxPity: json['last_pity'],
    jade: json['jade'],
    euro: json['euro'],
    id: json['id']
  );
}