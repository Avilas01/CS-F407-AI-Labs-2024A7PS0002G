from collections import deque

warehouse = [
    "#####################",
    "#S....#............G#",
    "#.##....##########..#",
    "#....##.............#",
    "#.######.###.#.###..#",
    "#........#..........#",
    "#####################"
]

rows = len(warehouse)
cols = len(warehouse[0])

start = None
goal = None

# Find S and G
for r in range(rows):
    for c in range(cols):
        if warehouse[r][c] == 'S':
            start = (r, c)
        elif warehouse[r][c] == 'G':
            goal = (r, c)

# Possible actions: Up, Down, Left, Right
directions = [
    (-1, 0, "Up"),
    (1, 0, "Down"),
    (0, -1, "Left"),
    (0, 1, "Right")
]


def bfs(start, goal):
    queue = deque([start])

    # Stores visited positions and how we reached them
    visited = {start: (None, None)}

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        r, c = current

        for dr, dc, action in directions:
            nr = r + dr
            nc = c + dc

            new_position = (nr, nc)

            # Check that the position is inside the grid
            # and is not an obstacle
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and warehouse[nr][nc] != '#'
                and new_position not in visited
            ):
                visited[new_position] = (current, action)
                queue.append(new_position)

    # No path exists
    if goal not in visited:
        return None, None

    # Reconstruct path
    path = []
    actions = []

    current = goal

    while current != start:
        path.append(current)

        previous, action = visited[current]
        actions.append(action)

        current = previous

    path.append(start)

    path.reverse()
    actions.reverse()

    return path, actions


path, actions = bfs(start, goal)

if path is None:
    print("No path exists.")
else:
    print("Path found!")
    print("Positions:")
    print(path)

    print("\nActions:")
    print(actions)

    print("\nNumber of moves:", len(actions))

    # Display path on warehouse map
    display = [list(row) for row in warehouse]

    for r, c in path:
        if display[r][c] not in ('S', 'G'):
            display[r][c] = '*'

    print("\nPath on warehouse:")
    for row in display:
        print("".join(row))