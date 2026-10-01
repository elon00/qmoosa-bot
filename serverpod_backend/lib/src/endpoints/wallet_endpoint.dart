import 'dart:async';
import 'package:serverpod/serverpod.dart';

/// Serverpod Endpoint for Dynamic QR Code generation and Multi-Wallet balances
class WalletEndpoint extends Endpoint {
  final Map<String, dynamic> _balances = {
    'algorand': {'balance': 142.50, 'token': 'ALGO', 'network': 'MainNet'},
    'solana': {'balance': 12.84, 'token': 'SOL', 'network': 'Mainnet-Beta'},
    'evm': {'balance': 1.45, 'token': 'ETH', 'network': 'Base'},
    'lightning': {'balance': 850000, 'token': 'SATS', 'network': 'Lightning'},
  };

  Future<Map<String, dynamic>> getBalances(Session session) async {
    return _balances;
  }

  Future<Map<String, dynamic>> generateDynamicQR(
    Session session, {
    required String rail, // 'UPI', 'SOLANA_PAY', 'ALGORAND'
    required double amount,
    required String currency,
    required String reference,
  }) async {
    String uri;
    if (rail == 'UPI') {
      uri = 'upi://pay?pa=qmoosabot@upi&pn=QmoosaBot&am=${amount.toStringAsFixed(2)}&cu=$currency&tr=$reference';
    } else if (rail == 'SOLANA_PAY') {
      uri = 'solana:7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU?amount=$amount&reference=$reference';
    } else {
      uri = 'algorand://QMOOSAZ72HVK3X7B4M9NLEK9QP4VXZ8N2A6KLR8Y9W2K8LMNO9Q?amount=${(amount * 1e6).toInt()}&note=$reference';
    }

    return {
      'rail': rail,
      'amount': amount,
      'currency': currency,
      'paymentUri': uri,
      'reference': reference,
      'createdAt': DateTime.now().toIso8601String(),
    };
  }
}
