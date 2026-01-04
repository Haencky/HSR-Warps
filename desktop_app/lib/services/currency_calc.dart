import 'dart:math';

class CurrencyCalc {
  static Map exchangeRate = <String, double>{
    'eur': 2.64,  // euro
    'usd': 2.64,  // us dollar
    'ukp': 2.64,  // uk pound
    'yen': 320,   // japanese yen
    'won': 3200,  // korean won
  };

  static double convert(int pulls, String currency) => (pulls * exchangeRate[currency]).roundToDouble() / pow(10, 2);
  
}