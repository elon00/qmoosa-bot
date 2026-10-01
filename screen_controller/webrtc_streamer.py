"""
Qmoosa Bot - WebRTC & Remote Screen Streamer
Handles real-time screen frame broadcasting to the Flutter desktop/mobile client
and supports 1-click human-in-the-loop manual takeover.
"""

from typing import Dict, List, Any, Optional
import time
import uuid
import logging

logger = logging.getLogger("ScreenStreamer")

class ScreenStreamer:
    """
    Manages low-latency WebRTC/WebSocket video streaming of the virtual desktop
    and bridges control events between the Flutter UI and the ScreenDriver.
    """

    def __init__(self, fps: int = 30):
        self.fps = fps
        self.session_id = f"stream_{uuid.uuid4().hex[:8]}"
        self.is_streaming = False
        self.manual_takeover_active = False
        self.connected_viewers: List[str] = []

    def start_stream(self) -> Dict[str, Any]:
        self.is_streaming = True
        logger.info(f"[ScreenStreamer] Virtual desktop stream started. Session: {self.session_id}")
        return {
            "status": "STREAMING",
            "session_id": self.session_id,
            "target_fps": self.fps,
            "stream_url": f"wss://stream.qmoosa.internal/{self.session_id}",
            "webrtc_ice_servers": [{"urls": "stun:stun.l.google.com:19302"}],
        }

    def stop_stream(self) -> Dict[str, Any]:
        self.is_streaming = False
        logger.info(f"[ScreenStreamer] Virtual desktop stream stopped for {self.session_id}")
        return {"status": "STOPPED", "session_id": self.session_id}

    def request_human_takeover(self, reason: str = "2FA_OR_CAPTCHA_DETECTED") -> Dict[str, Any]:
        """Pauses autonomous agent actions and transfers mouse/keyboard authority to user."""
        self.manual_takeover_active = True
        logger.warning(f"[ScreenStreamer] EMERGENCY HUMAN TAKEOVER TRIGGERED: {reason}")
        return {
            "alert": "HUMAN_TAKEOVER_REQUIRED",
            "reason": reason,
            "takeover_token": uuid.uuid4().hex,
            "timestamp": time.time(),
        }

    def release_human_takeover(self) -> Dict[str, Any]:
        """Restores autonomous control to the Qmoosa Bot Agent Mesh."""
        self.manual_takeover_active = False
        logger.info("[ScreenStreamer] Human takeover released. Restoring agent automation.")
        return {"status": "AGENT_CONTROL_RESTORED", "timestamp": time.time()}

    def get_status(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "is_streaming": self.is_streaming,
            "manual_takeover_active": self.manual_takeover_active,
            "fps": self.fps,
            "connected_viewers_count": len(self.connected_viewers),
        }
