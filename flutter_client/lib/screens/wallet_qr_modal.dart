import 'package:flutter/material.dart';

class WalletQrModal extends StatefulWidget {
  const WalletQrModal({super.key});

  @override
  State<WalletQrModal> createState() => _WalletQrModalState();
}

class _WalletQrModalState extends State<WalletQrModal> {
  String _selectedRail = 'UPI';
  final TextEditingController _amountController = TextEditingController(text: '2500');

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'MULTI-WALLET & DYNAMIC QR PAY RAILS',
            style: TextStyle(color: Color(0xFF00FF88), fontWeight: FontWeight.bold, fontSize: 16),
          ),
          const SizedBox(height: 16),
          // Balances Row
          Row(
            children: [
              _buildBalanceCard('Algorand MainNet', '142.50 ALGO', '500,000 QALGO', Colors.greenAccent),
              const SizedBox(width: 12),
              _buildBalanceCard('Solana Network', '12.84 SOL', '150,000 QMOOSA', Colors.cyanAccent),
              const SizedBox(width: 12),
              _buildBalanceCard('EVM Base', '1.45 ETH', '25,000 USDC', Colors.blueAccent),
              const SizedBox(width: 12),
              _buildBalanceCard('BTC Lightning', '850,000 SATS', '0 Pending', Colors.amberAccent),
            ],
          ),
          const SizedBox(height: 24),
          // Dynamic QR Generator Container
          Expanded(
            child: Row(
              children: [
                Expanded(
                  flex: 1,
                  child: Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: const Color(0xFF0E1526),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: const Color(0xFF1B253D)),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('GENERATE INVOICE QR', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 12),
                        DropdownButtonFormField<String>(
                          initialValue: _selectedRail,
                          decoration: const InputDecoration(
                            labelText: 'Payment Rail',
                            border: OutlineInputBorder(),
                          ),
                          items: const [
                            DropdownMenuItem(value: 'UPI', child: Text('Fiat: UPI Dynamic QR (India/Global)')),
                            DropdownMenuItem(value: 'SOLANA_PAY', child: Text('Crypto: Solana Pay')),
                            DropdownMenuItem(value: 'ALGORAND', child: Text('Crypto: Algorand x402 URI')),
                          ],
                          onChanged: (val) {
                            setState(() {
                              _selectedRail = val!;
                            });
                          },
                        ),
                        const SizedBox(height: 12),
                        TextField(
                          controller: _amountController,
                          decoration: const InputDecoration(
                            labelText: 'Amount',
                            border: OutlineInputBorder(),
                          ),
                        ),
                        const SizedBox(height: 16),
                        ElevatedButton.icon(
                          onPressed: () {
                            setState(() {});
                          },
                          icon: const Icon(Icons.qr_code),
                          label: const Text('UPDATE DYNAMIC QR'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: const Color(0xFF00FF88),
                            foregroundColor: Colors.black,
                            minimumSize: const Size(double.infinity, 44),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(width: 16),
                // QR Display Canvas
                Expanded(
                  flex: 1,
                  child: Container(
                    decoration: BoxDecoration(
                      color: const Color(0xFF0A0F1D),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: const Color(0xFF1B253D)),
                    ),
                    child: Center(
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Container(
                            padding: const EdgeInsets.all(16),
                            color: Colors.white,
                            child: Icon(Icons.qr_code_2, size: 140, color: Colors.grey[900]),
                          ),
                          const SizedBox(height: 12),
                          Text(
                            '$_selectedRail DYNAMIC QR: ${_amountController.text}',
                            style: const TextStyle(color: Color(0xFF00FF88), fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(height: 4),
                          const Text(
                            'Instant agent webhook release upon payment confirmation',
                            style: TextStyle(color: Colors.white38, fontSize: 11),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildBalanceCard(String title, String nativeBal, String tokenBal, Color accentColor) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: const Color(0xFF0E1526),
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: accentColor.withValues(alpha: 0.3)),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: TextStyle(color: accentColor, fontSize: 11, fontWeight: FontWeight.bold)),
            const SizedBox(height: 6),
            Text(nativeBal, style: const TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.bold)),
            Text(tokenBal, style: const TextStyle(color: Colors.white54, fontSize: 11)),
          ],
        ),
      ),
    );
  }
}
