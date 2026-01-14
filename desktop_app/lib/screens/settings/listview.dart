import 'package:desktop_app/services/settings_service.dart';
import 'package:flutter/material.dart';

class SettingsBody extends StatefulWidget {
  const SettingsBody({super.key});

  @override
  SettingsPageState createState() => SettingsPageState();
}

class SettingsPageState extends State<SettingsBody> {
  final _urlController = TextEditingController();
  final _portController = TextEditingController();
  String _selectedCurrency = '€';
  final Map<String,String> _currencies = {
  '€': 'EUR',
  '\$': 'USD',
  '¥': 'JPY',
  '£': 'GBP'
  };

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
      String? savedCurrency = settings['currency'];
      if (savedCurrency != null && _currencies.containsKey(savedCurrency)) {
        _selectedCurrency = savedCurrency;
      }
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
        items: _currencies.entries.map((dynamic value) => DropdownMenuItem<String>(value: value.key, child: Text('${value.key} (${value.value})'))).toList(), 
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
