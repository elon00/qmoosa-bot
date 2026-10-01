import 'dart:async';
import 'package:serverpod/serverpod.dart';

/// Serverpod Endpoint for live virtual desktop interaction,
/// mouse/keyboard event injection, and human takeover requests.
class ScreenControllerEndpoint extends Endpoint {
  bool _manualTakeoverActive = false;

  Future<Map<String, dynamic>> sendMouseAction(
    Session session, {
    required int x,
    required int y,
    required String actionType, // 'move', 'click', 'double_click'
    String button = 'left',
  }) async {
    session.log('Mouse action: $actionType at ($x, $y) with $button button');
    return {
      'success': true,
      'cursorPosition': [x, y],
      'action': actionType,
      'timestamp': DateTime.now().toIso8601String(),
    };
  }

  Future<Map<String, dynamic>> sendKeyboardAction(
    Session session, {
    required String text,
    bool humanJitter = true,
  }) async {
    session.log('Keyboard action: typed ${text.length} characters');
    return {
      'success': true,
      'characterCount': text.length,
      'jitterApplied': humanJitter,
      'timestamp': DateTime.now().toIso8601String(),
    };
  }

  Future<Map<String, dynamic>> toggleHumanTakeover(
    Session session, {
    required bool enable,
    String reason = 'MANUAL_INTERVENTION',
  }) async {
    _manualTakeoverActive = enable;
    session.log('Manual Takeover set to: $enable (Reason: $reason)');
    return {
      'manualTakeoverActive': _manualTakeoverActive,
      'reason': reason,
      'timestamp': DateTime.now().toIso8601String(),
    };
  }
}
