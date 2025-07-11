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

def get_neighbor(state):
    neighbors = []
    moves = {
        "Up" : (-1, 0),
        "Down": (1, 0),
        "Right": (0, 1),
        "Left": (0, -1)
    }

    x_blank, y_blank = -1, -1
    found = False
    for i in range(4):
        for j in range(4):
            if state[i][j] == 0:
                x_blank = i
                y_blank = j
                found =  True
                break
        if found == True:
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

def ida_star_puzzle(start_state, goal_state, pdb1, pdb2, pdb3, tiles1, tiles2, tiles3):
    bound = pdb_heuristic(start_state, pdb1, pdb2, pdb3, tiles1, tiles2, tiles3)

    path = {start_state}
    path_moves = []
    while True:
        t = ida_star_search(start_state, 0, bound, path, path_moves, goal_state, pdb1, pdb2, pdb3, tiles1, tiles2, tiles3)
        if isinstance(t, list):
            return t
        if t == float('inf'):
            return None
        bound = t 


def ida_star_search(state, g, bound, path, path_moves, goal_state, pdb1, pdb2, pdb3, tiles1, tiles2, tiles3):
    f = g + pdb_heuristic(state, pdb1, pdb2, pdb3, tiles1, tiles2, tiles3)
    if f > bound:
        return f
    if state == goal_state:
        return path_moves.copy()
    min_bound = float('inf')
    for neighbor, move in get_neighbor(state):
        if neighbor in path:
            continue
        path.add(neighbor)
        path_moves.append(move)
        t = ida_star_search(neighbor, g + 1, bound, path, path_moves, goal_state, pdb1, pdb2, pdb3, tiles1, tiles2, tiles3)
        if isinstance(t, list):
            return t
        if t < min_bound:
            min_bound = t
        path.remove(neighbor)
        path_moves.pop()
    return min_bound


