import 'package:flutter/material.dart';

class X402BazaarView extends StatelessWidget {
  const X402BazaarView({super.key});

  final List<Map<String, dynamic>> _services = const [
    {
      'title': 'CAPTCHA_BYPASS_AI',
      'provider': 'agent_solver_01',
      'price': '2,000 QALGO',
      'sla': '5s',
      'rating': '4.98',
    },
    {
      'title': 'EMAIL_AND_PHONE_VERIFIER',
      'provider': 'agent_verifier_02',
      'price': '5,000 QALGO',
      'sla': '10s',
      'rating': '5.00',
    },
    {
      'title': 'DEEP_INSTAGRAM_LEAD_EXTRACTOR',
      'provider': 'agent_osint_03',
      'price': '15,000 QALGO',
      'sla': '30s',
      'rating': '4.95',
    },
    {
      'title': 'QUANTUM_RESISTANT_NOTARIZATION',
      'provider': 'agent_pqc_04',
      'price': '8,000 QALGO',
      'sla': '3s',
      'rating': '5.00',
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                'x402 AUTONOMOUS AGENT BAZAAR',
                style: TextStyle(color: Color(0xFF00FF88), fontWeight: FontWeight.bold, fontSize: 16),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: Colors.blue.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(4),
                  border: Border.all(color: Colors.blue),
                ),
                child: const Text('RFC HTTP 402 PROTOCOL', style: TextStyle(color: Colors.blue, fontSize: 11)),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Expanded(
            child: ListView.builder(
              itemCount: _services.length,
              itemBuilder: (context, index) {
                final s = _services[index];
                return Card(
                  color: const Color(0xFF0E1526),
                  margin: const EdgeInsets.only(bottom: 12),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                    side: const BorderSide(color: Color(0xFF1B253D)),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              s['title']!,
                              style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              'Provider: ${s['provider']} • SLA: ${s['sla']} • ★ ${s['rating']}',
                              style: const TextStyle(color: Colors.white54, fontSize: 12),
                            ),
                          ],
                        ),
                        Row(
                          children: [
                            Text(
                              s['price']!,
                              style: const TextStyle(color: Color(0xFF00FF88), fontWeight: FontWeight.bold),
                            ),
                            const SizedBox(width: 14),
                            ElevatedButton(
                              onPressed: () {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  SnackBar(
                                    content: Text('x402 Payment Challenge Issued for ${s['title']}'),
                                    backgroundColor: const Color(0xFF1B253D),
                                  ),
                                );
                              },
                              style: ElevatedButton.styleFrom(
                                backgroundColor: const Color(0xFF00FF88),
                                foregroundColor: Colors.black,
                              ),
                              child: const Text('PROCURE'),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
