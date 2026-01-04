import 'dart:convert';

import 'package:http/http.dart' as http;

class ApiService {
  static String baseUrl = 'http://127.0.0.1:8000';

  static Future<http.Response> fetchApi(String endpoint) async => await http.get(Uri.parse('$baseUrl/$endpoint'));

  static Future<List<dynamic>> getGachaTypes() async {
    dynamic r = await fetchApi('gacha_types');
    List<dynamic> data = jsonDecode(r.body);
    return data;
  }
}