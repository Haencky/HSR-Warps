import 'dart:convert';

import 'package:desktop_app/services/settings_service.dart';
import 'package:http/http.dart' as http;

class ApiService {
  static const String itemIdsURL = 'https://haencky.github.io/HSR-Warps/itemIDs.json';

  static Future<http.Response> fetchApi(String endpoint) async { 
    final settings = await SettingsService.getSettings();
    final String url = settings['url']!;
    final String port = settings['port']!;

    return await http.get(Uri.parse('$url:$port/api/$endpoint'));
  }

  static Future<List<dynamic>> getGachaTypes() async {
    dynamic r = await fetchApi('gacha_types');
    List<dynamic> data = jsonDecode(r.body);
    return data;
  }

  static Future<http.Response> sendToApi(String endpoint, Map<String, String> body) async {
    final settings = await SettingsService.getSettings();
    final String url = settings['url']!;
    final String port = settings['port']!;

    return await http.post(
      Uri.parse('$url:$port/$endpoint/'),
      body: body
    ); 
  }

  static Future<http.Response> fetchItemIds() async => await http.get(Uri.parse(itemIdsURL));
}