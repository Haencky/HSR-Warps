import 'package:desktop_app/services/settings_service.dart';
import 'package:flutter/material.dart';

class SettingsBody extends StatefulWidget {
  const SettingsBody({super.key});

  @override
  _SettingsPageState createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsBody> {
  final _urlController = TextEditingController();
  final _portController = TextEditingController();
  String _selectedCurrency = '€ (EUR)';
  final List<Map<String, String>> _currencies = [{'€': 'EUR'}, {'\$': 'USD'}, {'¥': 'JPY'}, {'£': 'GBP'}];

  @override
  void initState() {
    super.initState();
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    final settings = await SettingsService.getSettings();
    setState(() {
      _urlController.text = settings['url']!;
      _portController.text = settings['port']!;
      _selectedCurrency = settings['currency']!;
    });
  }

  @override
  Widget build(BuildContext context) => ListView(
    padding: const EdgeInsets.all(16),
    children: [
      TextField(
        controller: _urlController,
        decoration: const InputDecoration(labelText: 'URL of Django Backend (e.g. http://127.0.0.1)'),
      ),
      SizedBox(height: 20),
      TextField(
        controller: _portController,
        decoration: const InputDecoration(labelText: 'Port (e.g. 8000)'),
        keyboardType: TextInputType.number,
      ),
      const SizedBox(height: 20),
      DropdownButtonFormField(
        initialValue: _selectedCurrency,
        items: _currencies.map((dynamic value) => DropdownMenuItem<String>(value: value.keys.first, child: Text('${value.keys.first} (${value.values.first})'))).toList(), 
        onChanged: (val) => setState(() => _selectedCurrency = val!),
        decoration: const InputDecoration(labelText: 'Currency'),
      ),
      const SizedBox(height: 30),
      ElevatedButton(
        onPressed: () async {
          await SettingsService.saveSettings(_urlController.text, _portController.text, _selectedCurrency);
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(_selectedCurrency)));
          Navigator.pop(context);
        },
        child: Text('Save')
      )
    ],
  );
}
