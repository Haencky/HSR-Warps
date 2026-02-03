import 'dart:math';

class CurrencyCalc {
  static Map exchangeRate = <String, double>{
    '€': 2.64,  // euro
    '\$': 2.64,  // us dollar
    '£': 2.64,  // uk pound
    '¥': 320,   // japanese yen
    //'won': 3200,  // korean won
  };

  static double convert(int pulls, String currency) => (pulls * exchangeRate[currency]).roundToDouble() / pow(10, 2);
  
}