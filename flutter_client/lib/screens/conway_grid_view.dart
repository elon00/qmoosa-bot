import 'package:flutter/material.dart';

class ConwayGridView extends StatefulWidget {
  const ConwayGridView({super.key});

  @override
  State<ConwayGridView> createState() => _ConwayGridViewState();
}

class _ConwayGridViewState extends State<ConwayGridView> {
  final int _gridSize = 12;
  late List<List<int>> _grid;
  int _generation = 14;

  @override
  void initState() {
    super.initState();
    _grid = List.generate(
      _gridSize,
      (x) => List.generate(_gridSize, (y) {
        if ((x == 4 && y == 4) || (x == 4 && y == 5) || (x == 5 && y == 4) || (x == 5 && y == 5)) {
          return 1; // Active Swarm
        }
        if (x == 8 && y == 8) return 2; // Mutating
        if (x == 2 && y == 9) return 3; // Self-Healing
        return 0; // Idle
      }),
    );
  }

  Color _getCellColor(int state) {
    switch (state) {
      case 1:
        return const Color(0xFF00FF88); // Active
      case 2:
        return const Color(0xFF00F0FF); // Mutating
      case 3:
        return Colors.orangeAccent; // Healing
      default:
        return const Color(0xFF131B2E); // Dead/Idle
    }
  }

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
              Text(
                'CONWAY AUTOMATON SWARM MATRIX (Gen: $_generation)',
                style: const TextStyle(color: Color(0xFF00FF88), fontWeight: FontWeight.bold, fontSize: 16),
              ),
              ElevatedButton.icon(
                onPressed: () {
                  setState(() {
                    _generation++;
                  });
                },
                icon: const Icon(Icons.refresh, size: 16),
                label: const Text('TRIGGER TICK'),
                style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF1B253D)),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Expanded(
            child: GridView.builder(
              gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: _gridSize,
                crossAxisSpacing: 6,
                mainAxisSpacing: 6,
              ),
              itemCount: _gridSize * _gridSize,
              itemBuilder: (context, index) {
                int x = index ~/ _gridSize;
                int y = index % _gridSize;
                int state = _grid[x][y];
                return Container(
                  decoration: BoxDecoration(
                    color: _getCellColor(state),
                    borderRadius: BorderRadius.circular(4),
                    border: Border.all(color: Colors.white10),
                  ),
                  child: Center(
                    child: Text(
                      state > 0 ? '$state' : '',
                      style: const TextStyle(color: Colors.black, fontWeight: FontWeight.bold, fontSize: 10),
                    ),
                  ),
                );
              },
            ),
          ),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: const Color(0xFF0E1526),
              borderRadius: BorderRadius.circular(8),
            ),
            child: const Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                Text('🟢 1: Active Swarm', style: TextStyle(color: Color(0xFF00FF88), fontSize: 12)),
                Text('🔵 2: Mutating Worker', style: TextStyle(color: Color(0xFF00F0FF), fontSize: 12)),
                Text('🟠 3: Self-Healing', style: TextStyle(color: Colors.orangeAccent, fontSize: 12)),
                Text('⬛ 0: Idle Matrix Slot', style: TextStyle(color: Colors.white38, fontSize: 12)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
