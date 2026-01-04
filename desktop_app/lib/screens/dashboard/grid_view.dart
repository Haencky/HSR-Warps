import 'dart:convert';

import 'package:desktop_app/services/currency_calc.dart';
import 'package:flutter/material.dart';

import 'package:desktop_app/services/api_service.dart' show ApiService;

Widget indexGridView() => Container(
  child: _buildMainContent(),
);



Widget _buildMainContent() {
  return FutureBuilder(
    future: ApiService.fetchApi(''),
    builder: (context, snapshot) {
      if (snapshot.connectionState == ConnectionState.waiting) {
        return const Center(child: CircularProgressIndicator());
      }
      if (snapshot.hasData && snapshot.data!.statusCode == 200) {
        final Map<String, dynamic> responseData = jsonDecode(snapshot.data!.body);
        final Map<String, dynamic> types = responseData['types'];
        return Container(
          padding: const EdgeInsets.all(10),
          child: Column(
            spacing: 20,
            children: types.keys.map((typeName) {
              final typeData = types[typeName];
              return Expanded(
                child: Row(
                  spacing: 5,
                  children: [
                    Expanded(
                      child: Stack(
                        children: [
                          Image.network(
                            "${ApiService.baseUrl}${typeData['last_win']['item_image']}",
                            fit: BoxFit.cover,
                            errorBuilder: (context, error, stackTrace) {
                              return Icon(Icons.broken_image, color: Colors.red);
                            },
                          ),
                          Container(
                            padding: const EdgeInsets.all(4),
                            decoration: BoxDecoration(
                              color: Colors.black87,
                            ),
                            child: Text(
                              '${typeData['c']}',
                              style: TextStyle(
                                color: Colors.white70
                              )
                            ),
                          )
                        ],
                      )
                    ),
                    Expanded(
                      flex: 2,
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            typeName,
                            style: const TextStyle(
                              fontSize: 32,
                            ),
                          ),
                          Row(
                            children: [
                              Text('5⭐ pity: ${typeData['pity']} / '),
                              Text('${typeData['max_pity']}',
                                style: TextStyle(
                                  color: typeData['warranted'] ? Colors.amber : Colors.red
                                )
                              ),
                            ]
                          ),
                          Text('${typeData['jade']} Jade (${CurrencyCalc.convert(typeData['jade'], 'eur')}€)'),
                          typeData['wr'] != null ? Text('Winrate: ${typeData['wr']}%') : Text('')
                        ]
                      )
                    )
                  ],
                )
              );
            }).toList(),
          )
        );
      }
      return const Center(child: Text('Error loading data'));
    },
  );
}