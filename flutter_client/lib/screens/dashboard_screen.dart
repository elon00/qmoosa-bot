import 'package:flutter/material.dart';
import 'screen_controller_view.dart';
import 'conway_grid_view.dart';
import 'x402_bazaar_view.dart';
import 'wallet_qr_modal.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  int _selectedTabIndex = 0;

  final List<Widget> _pages = const [
    ScreenControllerView(),
    ConwayGridView(),
    X402BazaarView(),
    WalletQrModal(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
              decoration: BoxDecoration(
                color: const Color(0xFF00FF88).withOpacity(0.2),
                borderRadius: BorderRadius.circular(6),
                border: Border.all(color: const Color(0xFF00FF88)),
              ),
              child: const Text(
                'QMOOSA BOT',
                style: TextStyle(
                  color: Color(0xFF00FF88),
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 1.2,
                ),
              ),
            ),
            const SizedBox(width: 14),
            const Text(
              'Autonomous Agentic OS • v1.0.0',
              style: TextStyle(fontSize: 13, color: Colors.white70),
            ),
          ],
        ),
        actions: [
          Container(
            margin: const EdgeInsets.symmetric(vertical: 10, horizontal: 12),
            padding: const EdgeInsets.symmetric(horizontal: 12),
            decoration: BoxDecoration(
              color: Colors.black45,
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: Colors.greenAccent),
            ),
            child: const Row(
              children: [
                Icon(Icons.lock, size: 14, color: Colors.greenAccent),
                SizedBox(width: 6),
                Text(
                  'PQC ML-KEM SECURE',
                  style: TextStyle(fontSize: 11, color: Colors.greenAccent),
                ),
              ],
            ),
          ),
        ],
      ),
      body: Row(
        children: [
          NavigationRail(
            backgroundColor: const Color(0xFF0A0F1D),
            selectedIndex: _selectedTabIndex,
            onDestinationSelected: (int index) {
              setState(() {
                _selectedTabIndex = index;
              });
            },
            labelType: NavigationRailLabelType.all,
            selectedIconTheme: const IconThemeData(color: Color(0xFF00FF88)),
            selectedLabelTextStyle: const TextStyle(color: Color(0xFF00FF88), fontSize: 11),
            unselectedLabelTextStyle: const TextStyle(color: Colors.white54, fontSize: 11),
            destinations: const [
              NavigationRailDestination(
                icon: Icon(Icons.desktop_windows_outlined),
                selectedIcon: Icon(Icons.desktop_windows),
                label: Text('Screen Control'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.grid_view_outlined),
                selectedIcon: Icon(Icons.grid_view),
                label: Text('Conway Swarm'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.storefront_outlined),
                selectedIcon: Icon(Icons.storefront),
                label: Text('x402 Bazaar'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.qr_code_2_outlined),
                selectedIcon: Icon(Icons.qr_code_2),
                label: Text('Wallet & QR'),
              ),
            ],
          ),
          const VerticalDivider(width: 1, thickness: 1, color: Color(0xFF1B253D)),
          Expanded(child: _pages[_selectedTabIndex]),
        ],
      ),
    );
  }
}
