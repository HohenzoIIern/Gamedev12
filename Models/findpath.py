from dataclasses import dataclass, field
from typing import Any
from copy import copy
from queue import PriorityQueue

def simple_path_finding(state):
    if state.turn == 1:
        return 100 * abs(state.player_one_pos[0])
    else:
        return 100 * (abs(state.player_two_pos[0] - 16))

def astar(game_state, check_blockage, heuristic=simple_path_finding):
    visited = set()

    def cost_function(my_path):
        actions = []
        current_cost = 0
        for state in my_path:
            current_cost += state[1][2]
        current_cost += len(actions)
        current_cost += heuristic(my_path[-1][0])
        return current_cost

    queue = PriorityQueue()
    if game_state.turn:
        pos = game_state.player_one_pos
    else:
        pos = game_state.player_two_pos
    queue.put(PriorityQueueItem(0, [(game_state, ((pos[0], pos[1]), (0, 0), 0))]))

    while not queue.empty():
        item = queue.get()
        path = item.item
        current_state = path[-1][0]
        current_simplified_state = path[-1][1]
        if current_state.is_goal_state():
            if check_blockage:
                return True
            final_path = []
            for state in path:
                final_path.append(state[1][1])
            return len(final_path[1:])
        if current_simplified_state not in visited:
            visited.add(current_simplified_state)
            for successor in current_state.get_child_states_with_moves():
                if successor[1] not in visited:
                    successor_path = copy(path)
                    successor_path.append(successor)
                    queue.put(PriorityQueueItem(cost_function(successor_path), successor_path))
    if check_blockage:
        return False
    return 0


@dataclass(order=True)
class PriorityQueueItem:
    priority: int
    item: Any = field(compare=False)
