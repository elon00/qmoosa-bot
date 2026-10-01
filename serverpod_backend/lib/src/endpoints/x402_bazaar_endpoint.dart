import 'dart:async';
import 'package:serverpod/serverpod.dart';

/// Serverpod Endpoint for x402 HTTP 402 Autonomous Agent Bazaar
class X402BazaarEndpoint extends Endpoint {
  final List<Map<String, dynamic>> _catalog = [
    {
      'serviceId': 'srv_captcha_01',
      'serviceName': 'CAPTCHA_BYPASS_AI',
      'costMicrounits': 2000,
      'token': 'QALGO',
      'slaSeconds': 5,
      'rating': 4.98,
    },
    {
      'serviceId': 'srv_verifier_02',
      'serviceName': 'EMAIL_AND_PHONE_VERIFIER',
      'costMicrounits': 5000,
      'token': 'QALGO',
      'slaSeconds': 10,
      'rating': 5.0,
    },
    {
      'serviceId': 'srv_osint_03',
      'serviceName': 'DEEP_INSTAGRAM_LEAD_EXTRACTOR',
      'costMicrounits': 15000,
      'token': 'QALGO',
      'slaSeconds': 30,
      'rating': 4.95,
    },
  ];

  Future<List<Map<String, dynamic>>> getAvailableServices(Session session) async {
    return _catalog;
  }

  Future<Map<String, dynamic>> createX402Order(
    Session session, {
    required String buyerAgentId,
    required String serviceId,
  }) async {
    final srv = _catalog.firstWhere((s) => s['serviceId'] == serviceId, orElse: () => _catalog.first);
    final orderId = 'ord_${DateTime.now().millisecondsSinceEpoch}';

    return {
      'orderId': orderId,
      'serviceName': srv['serviceName'],
      'amountMicro': srv['costMicrounits'],
      'token': srv['token'],
      'receiver': 'WALLET_AGENT_SERVICE_ALGORAND_MAINNET',
      'challengeHeaders': {
        'WWW-Authenticate': 'x402-Agent realm="${srv['serviceName']}"',
        'X-402-Blockchain': 'algorand',
        'X-402-Network': 'mainnet',
        'X-402-Amount': srv['costMicrounits'].toString(),
      },
      'status': 'PAYMENT_REQUIRED',
    };
  }
}
