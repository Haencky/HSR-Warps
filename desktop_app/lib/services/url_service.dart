import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:path/path.dart' as p;
import 'dart:io';

class OperatingSystem implements Exception {
  @override
  String toString() => 'Operating System is not supported';
}

class PlayerLog implements Exception {
  @override
  String toString() => 'Player.log not found';
}

class UserProfile implements Exception {
  @override
  String toString() => 'Userprofile is null';
}

class UrlService {
  
  static Future<String?> getUrl() async {
    RegExp pattern = RegExp(r'https://[^\x00]+/get(?:Ld)?GachaLog[^\x00]*');
    
    Uint8List? fileData = _getFileData();
    String strings = latin1.decode(fileData!);

    var match = pattern.allMatches(strings);
    if (match.isEmpty) return null;

    String? url = match.last.group(0);
    if (! await _verifyUrl(url!)) return 'No valid URL found, open Gacha Log in HSR';

    return url;
  }

  static Future<bool> _verifyUrl(String url) async {
    final response = await http.get(Uri.parse(url));
    if (response.statusCode == 200) {
      final Map<String, dynamic> responseBody = jsonDecode(response.body);
      if (responseBody['message'] == 'OK') return true;
    }
    return false;
  }

  static Uint8List? _getFileData() {
    String? installationPath = _getInstallationPath();

    if (installationPath == null) return null;

    final directory = Directory(p.join(installationPath, 'webCaches'));
    if (!directory.existsSync()) return null;
    List<FileSystemEntity> webCacheDir = directory.listSync();
    webCacheDir.sort((a,b) {
      String nameA = p.basename(a.path);  // directory name of one directory
      String nameB = p.basename(b.path);  // directory name of other directory 
      return nameB.compareTo(nameA);  // sort decreasing, highest first
    });
    String filePath = p.join(webCacheDir[0].path, 'Cache', 'Cache_Data', 'data_2');  // in data_2 the URL is stored     

    try {
      File f = File(filePath);
      return f.readAsBytesSync();
    } catch (e) {
      print('error loading file');
    }   
    return null;
  }

  static String? _getInstallationPath()  {
    if (Platform.isWindows) { // windows
      String? userProfile = Platform.environment['USERPROFILE']; 
      RegExp regex = RegExp(r'Loading player data from (.+)/data.unity3d');

      if (userProfile != null) {
        String targetPath = p.join(userProfile, 'AppData', 'LocalLow', 'Cognosphere', r'Star Rail', 'Player.log');
  

        try {
          File playerLog = File(targetPath);
          var content = playerLog.readAsLinesSync();
          for (var l in content) {
            if (regex.hasMatch(l)) {
              var installPath = regex.firstMatch(l);
              String? path = installPath!.group(1)?.trim();
              return path;
            }
          }
        } catch (e) {
          return 'Error loading player.log'; 
        }
      } else { 
        throw UserProfile();
      }
    } else {
      throw OperatingSystem();
    }
    return null;
  }
}