import heapq
import os
import pickle
from collections import deque


class PuzzleNode:
    def __init__(self, state, parent=None, move=None, depth=0, cost=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost
    def __lt__(self, other):
        return self.cost < other.cost


def get_neighbor(state):
    neighbors = []
    moves = {
        "Up" : (-1, 0),
        "Down": (1, 0),
        "Right": (0, 1),
        "Left": (0, -1)
    }

    x_blank, y_blank = -1, -1
    for i in range(4):
        for j in range(4):
            if state[i][j] == 0:
                x_blank = i
                y_blank = j
                break

    for move, (dx, dy) in moves.items():
        x_new = x_blank + dx
        y_new = y_blank + dy
        if 0 <= x_new < 4 and 0 <= y_new < 4:
            new_state = [list(row) for row in state]
            tmp = new_state[x_new][y_new]
            new_state[x_new][y_new] = new_state[x_blank][y_blank]
            new_state[x_blank][y_blank] = tmp
            neighbors.append((tuple(tuple(row) for row in new_state), move))
    return neighbors


def extract_pattern(state, pattern_tiles):
    pattern_state = []
    for row in state:
        new_row = []
        for tile in row:
            if tile == 0 or tile in pattern_tiles:
                new_row.append(tile)
            else:
                new_row.append(-1)
        pattern_state.append(tuple(new_row))
    return tuple(pattern_state)

def build_pattern_db(pattern_tiles, goal_state):
    pdb = {}
    goal_pattern = extract_pattern(goal_state, set(pattern_tiles))
    pdb[goal_pattern] = 0
    queue = deque()
    queue.append(goal_state)
    while queue:
        current = queue.popleft()
        current_cost = pdb[extract_pattern(current, set(pattern_tiles))]
        for neighbor, move in get_neighbor(current):
            neighbor_pattern = extract_pattern(neighbor, set(pattern_tiles))
            if neighbor_pattern not in pdb:
                pdb[neighbor_pattern] = current_cost + 1
                queue.append(neighbor)
    return pdb

def load_or_generate_pdb(goal_state, pattern_tiles, filename):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            pdb = pickle.load(f)
    else:
        pdb = build_pattern_db(pattern_tiles, goal_state)
        with open(filename, "wb") as f:
            pickle.dump(pdb, f)
    return pdb

def pdb_heuristic(state, pdb1, pdb2, pdb3, tiles1, tiles2, tiles3):
    h1 = pdb1.get(extract_pattern(state, set(tiles1)), 0)
    h2 = pdb2.get(extract_pattern(state, set(tiles2)), 0)
    h3 = pdb3.get(extract_pattern(state, set(tiles3)), 0)
    return h1 + h2 + h3

def astar_puzzle(start_state, goal_state, pdb1, pdb2, pdb3, tiles1, tiles2, tiles3):
    open_set = []
    closed_set = set()
    start_node = PuzzleNode(
        start_state,
        parent=None,
        move=None,
        depth=0,
        cost=pdb_heuristic(start_state, pdb1, pdb2, pdb3, tiles1, tiles2, tiles3)
    )
    heapq.heappush(open_set, start_node)
    while open_set:
        current_node = heapq.heappop(open_set)
        if current_node.state == goal_state:
            path = []
            while current_node:
                if current_node.move:
                    path.append(current_node.move)
                current_node = current_node.parent
            return path[::-1]
        closed_set.add(current_node.state)
        for neighbor_state, move in get_neighbor(current_node.state):
            if neighbor_state in closed_set:
                continue
            g_new = current_node.depth + 1
            h_new = pdb_heuristic(neighbor_state, pdb1, pdb2, pdb3, tiles1, tiles2, tiles3)
            new_node = PuzzleNode(
                neighbor_state,
                parent=current_node,
                move=move,
                depth=g_new,
                cost=g_new + h_new
            )
            heapq.heappush(open_set, new_node)
    return None

