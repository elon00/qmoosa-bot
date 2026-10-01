"""
Qmoosa Bot - Conway Automaton Workflow Engine
Implements cellular automata-based dynamic agent scheduling, emergent task decomposition,
and self-healing fault tolerance.
"""

from typing import Dict, List, Tuple, Any, Optional
import numpy as np
import time
import uuid
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ConwayAutomaton")

# Cellular States
STATE_DEAD = 0        # Terminated / Idle
STATE_ACTIVE = 1      # Executing Task
STATE_MUTATING = 2    # Overloaded -> Spawning sub-agent
STATE_HEALING = 3     # Self-healing / Error Recovery
STATE_COMPLETED = 4   # Successfully Finished


class AgentCell:
    def __init__(self, x: int, y: int, role: str = "Worker", task_id: Optional[str] = None):
        self.x = x
        self.y = y
        self.role = role
        self.task_id = task_id or str(uuid.uuid4())[:8]
        self.state = STATE_ACTIVE
        self.energy = 100
        self.memory: Dict[str, Any] = {}
        self.history: List[str] = []
        self.last_updated = time.time()

    def update_state(self, new_state: int, log_msg: str = ""):
        self.state = new_state
        self.last_updated = time.time()
        if log_msg:
            self.history.append(f"[{time.strftime('%X')}] {log_msg}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "coordinate": [self.x, self.y],
            "role": self.role,
            "task_id": self.task_id,
            "state": self.state,
            "energy": self.energy,
            "history": self.history[-5:],
            "last_updated": self.last_updated,
        }


class ConwayAutomatonEngine:
    """
    Cellular Automata Engine that coordinates emergent multi-agent operations.
    Applies Game of Life rules adapted for autonomous task swarms.
    """

    def __init__(self, grid_size: int = 16):
        self.grid_size = grid_size
        self.grid = np.zeros((grid_size, grid_size), dtype=int)
        self.cells: Dict[Tuple[int, int], AgentCell] = {}
        self.generation = 0
        self.active_tasks_queue: List[Dict[str, Any]] = []

    def spawn_agent(self, x: int, y: int, role: str, task_payload: Dict[str, Any]) -> AgentCell:
        x, y = x % self.grid_size, y % self.grid_size
        cell = AgentCell(x, y, role=role)
        cell.memory = task_payload
        cell.history.append(f"Spawned role '{role}' for task {cell.task_id}")
        self.cells[(x, y)] = cell
        self.grid[x, y] = STATE_ACTIVE
        logger.info(f"[ConwayEngine] Agent '{role}' spawned at ({x}, {y}) [Task: {cell.task_id}]")
        return cell

    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = (x + dx) % self.grid_size, (y + dy) % self.grid_size
                neighbors.append((nx, ny))
        return neighbors

    def count_active_neighbors(self, x: int, y: int) -> int:
        neighbors = self.get_neighbors(x, y)
        active_count = 0
        for nx, ny in neighbors:
            if self.grid[nx, ny] in [STATE_ACTIVE, STATE_MUTATING]:
                active_count += 1
        return active_count

    def tick(self) -> Dict[str, Any]:
        """
        Executes one evolutionary step across the multi-agent lattice.
        Applies Conway's Agentic Life Rules:
        1. Isolation/Underpopulation (< 2 active neighbors): Agent consolidates context.
        2. Optimal Swarm (2-3 active neighbors): High-throughput parallel execution.
        3. Overcrowding (> 3 active neighbors): Triggers task mutation / sub-agent delegation.
        4. Rebirth/Self-Healing (dead cell with 3 active neighbors): Emergent worker revival.
        """
        self.generation += 1
        new_grid = self.grid.copy()
        transitions = []

        # 1. Update Existing Cells
        for (x, y), cell in list(self.cells.items()):
            active_nbrs = self.count_active_neighbors(x, y)

            if cell.state == STATE_ACTIVE:
                if active_nbrs < 2:
                    # Underpopulation: Consolidate or rest
                    cell.energy = max(0, cell.energy - 5)
                    if cell.energy == 0:
                        cell.update_state(STATE_DEAD, "Cell depowered due to isolation")
                        new_grid[x, y] = STATE_DEAD
                        transitions.append(f"Agent ({x},{y}) died of isolation")
                elif active_nbrs in [2, 3]:
                    # Thriving: Steady progress
                    cell.energy = min(100, cell.energy + 10)
                    cell.history.append(f"Gen {self.generation}: Thriving with {active_nbrs} collaborators")
                elif active_nbrs > 3:
                    # Overpopulation: High task load -> Mutate & delegate
                    cell.update_state(STATE_MUTATING, f"Gen {self.generation}: Overcrowded ({active_nbrs} nbrs), delegating")
                    new_grid[x, y] = STATE_MUTATING
                    transitions.append(f"Agent ({x},{y}) mutating to relieve swarm load")

            elif cell.state == STATE_MUTATING:
                # Spawn a child worker in an open adjacent cell
                open_slots = [pt for pt in self.get_neighbors(x, y) if self.grid[pt[0], pt[1]] == STATE_DEAD]
                if open_slots:
                    cx, cy = open_slots[0]
                    child = AgentCell(cx, cy, role="SubWorker", task_id=f"{cell.task_id}_sub")
                    self.cells[(cx, cy)] = child
                    new_grid[cx, cy] = STATE_ACTIVE
                    cell.update_state(STATE_ACTIVE, f"Spawned SubWorker at ({cx},{cy})")
                    new_grid[x, y] = STATE_ACTIVE
                    transitions.append(f"Mutated cell ({x},{y}) spawned child at ({cx},{cy})")
                else:
                    cell.update_state(STATE_ACTIVE, "No slots to spawn child; resumed work")
                    new_grid[x, y] = STATE_ACTIVE

            elif cell.state == STATE_HEALING:
                # Successfully recovered
                cell.energy = 100
                cell.update_state(STATE_ACTIVE, "Self-healing routine complete")
                new_grid[x, y] = STATE_ACTIVE
                transitions.append(f"Agent ({x},{y}) recovered from failure")

        # 2. Rebirth & Self-Healing Scan
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x, y] == STATE_DEAD:
                    active_nbrs = self.count_active_neighbors(x, y)
                    if active_nbrs == 3:
                        # Emergence rule: Revive cell
                        revived = AgentCell(x, y, role="HealerOrchestrator")
                        revived.update_state(STATE_ACTIVE, "Emerged via Conway rule (3 active neighbors)")
                        self.cells[(x, y)] = revived
                        new_grid[x, y] = STATE_ACTIVE
                        transitions.append(f"Emergent agent materialized at ({x},{y})")

        self.grid = new_grid
        return {
            "generation": self.generation,
            "active_cells_count": int(np.sum(self.grid == STATE_ACTIVE)),
            "mutating_count": int(np.sum(self.grid == STATE_MUTATING)),
            "transitions": transitions,
        }

    def trigger_failure(self, x: int, y: int, error_reason: str):
        """Simulate an external failure (e.g., CAPTCHA, Rate-Limit, IP Block)"""
        if (x, y) in self.cells:
            cell = self.cells[(x, y)]
            cell.update_state(STATE_HEALING, f"Triggered self-healing due to: {error_reason}")
            self.grid[x, y] = STATE_HEALING
            logger.warning(f"[ConwayEngine] Agent at ({x},{y}) entering self-healing: {error_reason}")

    def get_matrix_snapshot(self) -> List[List[int]]:
        return self.grid.tolist()

    def get_all_agents(self) -> List[Dict[str, Any]]:
        return [cell.to_dict() for cell in self.cells.values() if cell.state != STATE_DEAD]
