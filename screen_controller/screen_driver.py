"""
Qmoosa Bot - OS & Browser Screen Driver
Provides high-fidelity, anti-detect mouse movement with Bézier curve smoothing,
human-like keystroke jitter, and virtual desktop interaction primitives.
"""

from typing import Dict, List, Tuple, Any, Optional
import time
import random
import math
import logging
from screen_controller.visual_grounding import VisualGroundingEngine

logger = logging.getLogger("ScreenDriver")

class ScreenDriver:
    """
    Simulates human-level OS desktop and browser interaction.
    Features:
    - Cubic Bézier mouse movement paths to evade bot detection.
    - Gaussian typing delays for natural text streaming.
    - Viewport inspection and action audit trail.
    """

    def __init__(self, viewport: Tuple[int, int] = (1920, 1080)):
        self.width, self.height = viewport
        self.cursor_x = self.width // 2
        self.cursor_y = self.height // 2
        self.grounding = VisualGroundingEngine(self.width, self.height)
        self.action_history: List[Dict[str, Any]] = []

    def calculate_bezier_trajectory(self, start: Tuple[int, int], end: Tuple[int, int], steps: int = 15) -> List[Tuple[int, int]]:
        """
        Generates a human-like cubic Bézier curve between start and target points.
        Bypasses simplistic linear movement anti-bot detectors.
        """
        x0, y0 = start
        x3, y3 = end
        # Generate pseudo-random control points
        dx, dy = x3 - x0, y3 - y0
        ctrl_dist = math.hypot(dx, dy) * 0.3
        angle = math.atan2(dy, dx) + random.uniform(-0.4, 0.4)

        x1 = int(x0 + math.cos(angle) * ctrl_dist)
        y1 = int(y0 + math.sin(angle) * ctrl_dist)

        x2 = int(x3 - math.cos(angle) * ctrl_dist)
        y2 = int(y3 - math.sin(angle) * ctrl_dist)

        trajectory = []
        for i in range(steps + 1):
            t = i / steps
            # Cubic Bézier formula
            bx = (1 - t)**3 * x0 + 3 * (1 - t)**2 * t * x1 + 3 * (1 - t) * t**2 * x2 + t**3 * x3
            by = (1 - t)**3 * y0 + 3 * (1 - t)**2 * t * y1 + 3 * (1 - t) * t**2 * y2 + t**3 * y3
            trajectory.append((int(bx), int(by)))
        return trajectory

    def move_mouse(self, target_x: int, target_y: int, smooth: bool = True) -> Dict[str, Any]:
        target_x = max(0, min(self.width, target_x))
        target_y = max(0, min(self.height, target_y))

        if smooth:
            points = self.calculate_bezier_trajectory((self.cursor_x, self.cursor_y), (target_x, target_y))
            for pt in points:
                self.cursor_x, self.cursor_y = pt
                time.sleep(random.uniform(0.005, 0.015))  # Micro-jitter
        else:
            self.cursor_x, self.cursor_y = target_x, target_y

        action = {"action": "mouse_move", "position": [self.cursor_x, self.cursor_y], "timestamp": time.time()}
        self.action_history.append(action)
        logger.info(f"[ScreenDriver] Mouse moved to ({self.cursor_x}, {self.cursor_y})")
        return action

    def click(self, target_x: Optional[int] = None, target_y: Optional[int] = None, button: str = "left") -> Dict[str, Any]:
        if target_x is not None and target_y is not None:
            self.move_mouse(target_x, target_y, smooth=True)

        # Micro-pause before click
        time.sleep(random.uniform(0.04, 0.09))
        action = {"action": "click", "button": button, "position": [self.cursor_x, self.cursor_y], "timestamp": time.time()}
        self.action_history.append(action)
        logger.info(f"[ScreenDriver] Click executed ({button}) at ({self.cursor_x}, {self.cursor_y})")
        return action

    def type_text(self, text: str, human_jitter: bool = True) -> Dict[str, Any]:
        typed = []
        for char in text:
            typed.append(char)
            if human_jitter:
                # 45ms to 110ms typing rhythm
                delay = random.gauss(0.06, 0.015)
                time.sleep(max(0.02, min(0.15, delay)))

        action = {
            "action": "type_text",
            "length": len(text),
            "preview": text[:30] + ("..." if len(text) > 30 else ""),
            "timestamp": time.time(),
        }
        self.action_history.append(action)
        logger.info(f"[ScreenDriver] Typed string (len={len(text)}) with human cadence.")
        return action

    def navigate_and_interact(self, target_query: str, context: str = "instagram_dm", payload_text: Optional[str] = None) -> Dict[str, Any]:
        """
        End-to-end visual execution:
        1. Locate target coordinate via Visual Grounding
        2. Move cursor along natural Bézier curve
        3. Click target
        4. If text payload provided, type with natural jitter
        """
        coords = self.grounding.find_target_coordinate(target_query, context)
        if not coords:
            return {"success": False, "error": f"Element '{target_query}' not located"}

        tx, ty = coords
        move_res = self.move_mouse(tx, ty, smooth=True)
        click_res = self.click(tx, ty)

        type_res = None
        if payload_text:
            type_res = self.type_text(payload_text, human_jitter=True)

        return {
            "success": True,
            "target": target_query,
            "grounded_coordinate": [tx, ty],
            "move": move_res,
            "click": click_res,
            "typing": type_res,
        }
