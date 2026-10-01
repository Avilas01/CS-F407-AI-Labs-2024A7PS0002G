import heapq
from collections import deque
import math


# =========================================================
# Helper functions
# =========================================================

def find_positions(grid):
    start = None
    goal = None

    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == "S":
                start = (r, c)
            elif grid[r][c] == "G":
                goal = (r, c)

    return start, goal


def get_neighbors(grid, position):
    r, c = position

    directions = [
        (-1, 0),   # Up
        (1, 0),    # Down
        (0, -1),   # Left
        (0, 1)     # Right
    ]

    neighbors = []

    for dr, dc in directions:
        nr = r + dr
        nc = c + dc

        if (
            0 <= nr < len(grid)
            and 0 <= nc < len(grid[0])
            and grid[nr][nc] != "#"
        ):
            neighbors.append((nr, nc))

    return neighbors


def reconstruct_path(parent, start, goal):
    path = []
    current = goal

    while current != start:
        path.append(current)
        current = parent[current]

    path.append(start)
    path.reverse()

    return path


# =========================================================
# Heuristics
# =========================================================

def zero_heuristic(a, b):
    return 0


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean(a, b):
    return math.sqrt(
        (a[0] - b[0]) ** 2 +
        (a[1] - b[1]) ** 2
    )


def double_manhattan(a, b):
    return 2 * manhattan(a, b)


# =========================================================
# A* Search
# =========================================================

def astar(grid, heuristic=manhattan):
    start, goal = find_positions(grid)

    frontier = []
    heapq.heappush(frontier, (0, start))

    parent = {}
    g_cost = {start: 0}
    visited = set()

    states_expanded = 0

    while frontier:
        f, current = heapq.heappop(frontier)

        if current in visited:
            continue

        visited.add(current)
        states_expanded += 1

        if current == goal:
            path = reconstruct_path(parent, start, goal)

            return {
                "found": True,
                "path": path,
                "length": len(path) - 1,
                "expanded": states_expanded
            }

        for neighbor in get_neighbors(grid, current):

            new_g = g_cost[current] + 1

            if neighbor not in g_cost or new_g < g_cost[neighbor]:

                g_cost[neighbor] = new_g

                h = heuristic(neighbor, goal)

                f = new_g + h

                heapq.heappush(frontier, (f, neighbor))

                parent[neighbor] = current

    return {
        "found": False,
        "path": None,
        "length": None,
        "expanded": states_expanded
    }


# =========================================================
# BFS Search
# =========================================================

def bfs(grid):
    start, goal = find_positions(grid)

    frontier = deque([start])

    parent = {}
    visited = {start}

    states_expanded = 0

    while frontier:
        current = frontier.popleft()

        states_expanded += 1

        if current == goal:
            path = reconstruct_path(parent, start, goal)

            return {
                "found": True,
                "path": path,
                "length": len(path) - 1,
                "expanded": states_expanded
            }

        for neighbor in get_neighbors(grid, current):

            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                frontier.append(neighbor)

    return {
        "found": False,
        "path": None,
        "length": None,
        "expanded": states_expanded
    }


# =========================================================
# Display result
# =========================================================

def print_result(name, result):

    print("\n", name)
    print("-" * 50)

    print("Solution found:", result["found"])
    print("Path length:", result["length"])
    print("States expanded:", result["expanded"])

    if result["found"]:
        print("Path:")
        print(result["path"])


# =========================================================
# ORIGINAL WAREHOUSE
# =========================================================

warehouse = [
    "#################",
    "#S....#.........#",
    "#.###.#.#######.#",
    "#...#.#.......#.#",
    "###.#.#######.#.#",
    "#...#.........#.#",
    "#.###########.#.#",
    "#.............#G#",
    "#################"
]


# =========================================================
# TASK 3 - TEST THE GENERATED PROGRAM
# =========================================================

print("\n================ TASK 3 ================")


# Test 1: Original warehouse

result = astar(warehouse)

print_result(
    "Test 1 - Original Warehouse",
    result
)


# Test 2: Trivial case

trivial_map = [
    "#####",
    "#SG##",
    "#####"
]

result = astar(trivial_map)

print_result(
    "Test 2 - Trivial Case",
    result
)


# Test 3: No solution

no_solution_map = [
    "#######",
    "#S....#",
    "###.###",
    "#...#G#",
    "#######"
]

result = astar(no_solution_map)

print_result(
    "Test 3 - No Solution",
    result
)


# Test 4: Alternative paths

alternative_map = [
    "#########",
    "#S......#",
    "#.......#",
    "#......G#",
    "#########"
]

result = astar(alternative_map)

print_result(
    "Test 4 - Alternative Paths",
    result
)


# =========================================================
# TASK 5 - BFS VS A*
# =========================================================

print("\n================ TASK 5 ================")

bfs_result = bfs(warehouse)

astar_result = astar(
    warehouse,
    manhattan
)

print_result(
    "BFS",
    bfs_result
)

print_result(
    "A*",
    astar_result
)


print("\nComparison")

print(
    "BFS path length:",
    bfs_result["length"]
)

print(
    "A* path length:",
    astar_result["length"]
)

print(
    "BFS states expanded:",
    bfs_result["expanded"]
)

print(
    "A* states expanded:",
    astar_result["expanded"]
)


# =========================================================
# TASK 6 - HEURISTIC INVESTIGATION
# =========================================================

print("\n================ TASK 6 ================")

heuristics = [
    ("h(n) = 0", zero_heuristic),

    (
        "Manhattan distance",
        manhattan
    ),

    (
        "Euclidean distance",
        euclidean
    ),

    (
        "2 x Manhattan distance",
        double_manhattan
    )
]


for name, heuristic in heuristics:

    result = astar(
        warehouse,
        heuristic
    )

    print_result(
        name,
        result
    )