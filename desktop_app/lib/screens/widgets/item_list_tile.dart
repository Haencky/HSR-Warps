import 'package:flutter/material.dart';

class ItemListTile extends StatelessWidget {
  final Map<String, dynamic> item;
  final String baseUrl;
  static const Map<int, dynamic> rarityColors = {
    3: Colors.lightBlue,
    4: Colors.deepPurple,
    5: Colors.amber
  };

  const ItemListTile({
    super.key,
    required this.item,
    required this.baseUrl
  });

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.symmetric(vertical: 6, horizontal: 12),
    child: Container(
      decoration: BoxDecoration(
        border: Border.all(
          color: rarityColors[item['rarity']],
          width: 2
        )
      ),
      child: Row(
        children: [
          ClipRRect(
            borderRadius: const BorderRadius.horizontal(left: Radius.circular(12)),
            child: Container(
              padding: EdgeInsets.all(10),
              child: Image.network(
                '$baseUrl${item['image']}',
                width: 375,
                height: 500,
                fit: BoxFit.cover
              ),
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Container(
              decoration: BoxDecoration(
                /*border: Border.all(
                  color: Colors.black,
                  width: 2
                )*/
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Text(
                    item['name'],
                    style: const TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 20
                    ),
                  ),
                  Text(
                    item['eng_name'] != item['name']
                    ? item['eng_name']
                    : '',
                    style: const TextStyle(
                      fontSize: 20
                    ),
                  )
                ],
              )
            ),
          ),
          ClipOval(
            child: Image.network(
              '$baseUrl${item['path_icon']}',
              width: 250,
              height: 250,
              fit: BoxFit.cover,
              color: Colors.black54,
            )
          )
        ],
      ),
    )
  );
}