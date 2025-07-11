class PuzzleNode:
    def __init__(self, state, parent=None, move=None, depth=0, cost=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost
    def __lt__(self, other):
        return self.cost < other.cost

def get_goal_position(goal_state):
    goal_positions = {}
    for i in range(4):
        for j in range(4):
            goal_positions[goal_state[i][j]] = (i, j)
    return goal_positions

def manhattan_distance(state, goal_positions):
    distance = 0
    for i in range(4):
        for j in range(4):
            if state[i][j] != 0:
                x_goal, y_goal = goal_positions[state[i][j]]
                distance += abs(i - x_goal) + abs(j - y_goal)
    return distance

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

def ida_star_puzzle(start_state, goal_state):
    goal_positions = get_goal_position(goal_state)
    bound = manhattan_distance(start_state, goal_positions)

    path = {start_state}
    path_moves = []
    while True:
        t = ida_star_search(start_state, 0, bound, path, path_moves, goal_state, goal_positions)
        if isinstance(t, list):
            return t
        if t == float('inf'):
            return None
        bound = t 

def ida_star_search(state, g, bound, path, path_moves, goal_state, goal_positions):
    f = g + manhattan_distance(state, goal_positions)
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
        t = ida_star_search(neighbor, g + 1, bound, path, path_moves, goal_state, goal_positions)
        if isinstance(t, list):
            return t
        if t < min_bound:
            min_bound = t
        path.remove(neighbor)
        path_moves.pop()
    return min_bound


