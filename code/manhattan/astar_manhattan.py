import heapq

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

def astar_puzzle(start_state, goal_state):
    open_set = []
    closed_set = set()
    goal_positions = get_goal_position(goal_state)

    start_node = PuzzleNode(
        start_state,
        parent=None,
        move=None,
        depth=0,
        cost=manhattan_distance(start_state, goal_positions)
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
            h_new = manhattan_distance(neighbor_state, goal_positions)
            new_node = PuzzleNode(
                neighbor_state,
                parent=current_node,
                move=move,
                depth=g_new,
                cost=g_new + h_new
            )
            heapq.heappush(open_set, new_node)
    return None

    

