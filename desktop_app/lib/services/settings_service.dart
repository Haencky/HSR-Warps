import 'package:shared_preferences/shared_preferences.dart';

class SettingsService {
  static const String _keyBaseUrl = 'base_url';
  static const String _keyPort = 'port';
  static const String _keyCurrency = 'currency';

  static const String defaultUrl = 'http://127.0.0.1';
  static const String defaultPort = '8000';

  static Future<void> saveSettings(String url, String port, String currency) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyBaseUrl, url);
    await prefs.setString(_keyPort, port);
    await prefs.setString(_keyCurrency, currency);
  }

  static Future<Map<String, String>> getSettings() async {
    final prefs = await SharedPreferences.getInstance();
    return {
      'url': prefs.getString(_keyBaseUrl) ?? defaultUrl,
      'port': prefs.getString(_keyPort) ?? defaultPort,
      'currency': prefs.getString(_keyCurrency) ?? '€ (EUR)'
    };
  }
}