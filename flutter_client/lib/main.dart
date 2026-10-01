import 'package:flutter/material.dart';
import 'screens/dashboard_screen.dart';

void main() {
  runApp(const QmoosaBotApp());
}

class QmoosaBotApp extends StatelessWidget {
  const QmoosaBotApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Qmoosa Bot - Agentic OS',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF070B14),
        primaryColor: const Color(0xFF00FF88),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF00FF88),
          secondary: Color(0xFF00F0FF),
          surface: Color(0xFF0E1526),
        ),
        fontFamily: 'monospace',
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF0E1526),
          elevation: 0,
        ),
      ),
      home: const DashboardScreen(),
    );
  }
}
