import 'package:flutter/material.dart';

class ScreenControllerView extends StatefulWidget {
  const ScreenControllerView({super.key});

  @override
  State<ScreenControllerView> createState() => _ScreenControllerViewState();
}

class _ScreenControllerViewState extends State<ScreenControllerView> {
  Offset _cursorPos = const Offset(450, 280);
  bool _manualTakeover = false;
  final List<String> _eventLogs = [
    '[ScreenController] Virtual Xvfb display 1920x1080 initialized.',
    '[VisionGrounding] Located "Send Message Input" at (450, 680).',
    '[ScreenDriver] Bézier curve trajectory calculated (15 steps).',
    '[Agent] Typing personalized outreach copy with human jitter.',
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
                'LIVE VIRTUAL DESKTOP STREAM',
                style: TextStyle(color: Color(0xFF00FF88), fontWeight: FontWeight.bold, fontSize: 16),
              ),
              Row(
                children: [
                  ElevatedButton.icon(
                    onPressed: () {
                      setState(() {
                        _manualTakeover = !_manualTakeover;
                        _eventLogs.add(_manualTakeover
                            ? '[ALERT] Human takeover requested. Pausing agent control.'
                            : '[STATUS] Human takeover released. Restoring agent swarm.');
                      });
                    },
                    icon: Icon(_manualTakeover ? Icons.lock_open : Icons.pan_tool, size: 16),
                    label: Text(_manualTakeover ? 'RELEASE TAKEOVER' : 'REQUEST 1-CLICK TAKEOVER'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: _manualTakeover ? Colors.amber[800] : const Color(0xFF1B253D),
                      foregroundColor: Colors.white,
                    ),
                  ),
                ],
              ),
            ],
          ),
          const SizedBox(height: 12),
          // Interactive Desktop Canvas
          Expanded(
            flex: 3,
            child: Container(
              width: double.infinity,
              decoration: BoxDecoration(
                color: Colors.black,
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: _manualTakeover ? Colors.amber : const Color(0xFF1B253D), width: 2),
              ),
              child: Stack(
                children: [
                  // Simulated Browser UI
                  Positioned.fill(
                    child: Padding(
                      padding: const EdgeInsets.all(24.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                            decoration: BoxDecoration(
                              color: const Color(0xFF131B2E),
                              borderRadius: BorderRadius.circular(6),
                            ),
                            child: const Row(
                              children: [
                                Icon(Icons.lock, size: 12, color: Colors.greenAccent),
                                SizedBox(width: 8),
                                Text(
                                  'https://instagram.com/direct/inbox',
                                  style: TextStyle(color: Colors.white70, fontSize: 12),
                                ),
                              ],
                            ),
                          ),
                          const Spacer(),
                          Center(
                            child: Column(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                const Icon(Icons.send_rounded, size: 48, color: Color(0xFF00FF88)),
                                const SizedBox(height: 12),
                                Text(
                                  _manualTakeover ? 'MANUAL CONTROL ACTIVE' : 'AUTONOMOUS SCREEN DRIVER OPERATING',
                                  style: TextStyle(
                                    color: _manualTakeover ? Colors.amber : Colors.white60,
                                    fontSize: 14,
                                    letterSpacing: 1.1,
                                  ),
                                ),
                              ],
                            ),
                          ),
                          const Spacer(),
                        ],
                      ),
                    ),
                  ),
                  // Animated Simulated Cursor
                  Positioned(
                    left: _cursorPos.dx,
                    top: _cursorPos.dy,
                    child: const Icon(
                      Icons.navigation,
                      color: Color(0xFF00FF88),
                      size: 20,
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 12),
          // Live Action Logs
          Expanded(
            flex: 1,
            child: Container(
              width: double.infinity,
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: const Color(0xFF0A0F1D),
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: const Color(0xFF1B253D)),
              ),
              child: ListView.builder(
                itemCount: _eventLogs.length,
                itemBuilder: (context, index) {
                  return Padding(
                    padding: const EdgeInsets.symmetric(vertical: 2.0),
                    child: Text(
                      _eventLogs[index],
                      style: const TextStyle(color: Colors.greenAccent, fontSize: 12),
                    ),
                  );
                },
              ),
            ),
          ),
        ],
      ),
    );
  }
}
