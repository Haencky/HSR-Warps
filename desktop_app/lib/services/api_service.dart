import 'dart:convert';

import 'package:desktop_app/services/settings_service.dart';
import 'package:http/http.dart' as http;

class ApiService {
  static String baseUrl = 'http://127.0.0.1:8000';

  static Future<http.Response> fetchApi(String endpoint) async { 
    final settings = await SettingsService.getSettings();
    final String url = settings['url']!;
    final String port = settings['port']!;

    return await http.get(Uri.parse('$url:$port/$endpoint'));
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
}