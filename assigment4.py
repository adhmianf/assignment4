terrain_grid = [
    ['S', 1,   2,   3,   '#',  5,   6],
    [1,   '#', 3,   '#',  6,   '#', 7],
    [2,   2,   3,   4,   5,   6,   8],
    ['#', 4,   '#', '#',  6,   '#', 7],
    [3,   2,   1,   2,   3,   4,  'G']
]

import heapq, time

ROWS, COLS = len(terrain_grid), len(terrain_grid[0])

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_pos(symbol):
    for i in range(ROWS):
        for j in range(COLS):
            if terrain_grid[i][j] == symbol:
                return (i, j)
    return None

def get_cost(pos):
    val = terrain_grid[pos[0]][pos[1]]
    return int(val) if isinstance(val, int) or val.isdigit() else 1

def is_valid(pos):
    i, j = pos
    return 0 <= i < ROWS and 0 <= j < COLS and terrain_grid[i][j] != '#'

def get_neighbors(pos):
    i, j = pos
    for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
        ni, nj = i + di, j + dj
        if is_valid((ni, nj)):
            yield (ni, nj)

def a_star(start, goal):
    frontier = [(0 + manhattan(start, goal), 0, start, [start])]
    visited = set()
    nodes = 0

    while frontier:
        f, g, current, path = heapq.heappop(frontier)
        nodes += 1

        if current == goal:
            return path, nodes

        if current in visited:
            continue
        visited.add(current)

        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                new_g = g + get_cost(neighbor)
                h = manhattan(neighbor, goal)
                heapq.heappush(frontier, (new_g + h, new_g, neighbor, path + [neighbor]))

    return None, nodes

def gbfs(start, goal):
    frontier = [(manhattan(start, goal), start, [start])]
    visited = set()
    nodes = 0

    while frontier:
        h, current, path = heapq.heappop(frontier)
        nodes += 1

        if current == goal:
            return path, nodes

        if current in visited:
            continue
        visited.add(current)

        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                heapq.heappush(frontier, (manhattan(neighbor, goal), neighbor, path + [neighbor]))

    return None, nodes

def print_grid_path(grid, path):
    new_grid = [[str(cell) for cell in row] for row in grid]
    for i, j in path:
        if new_grid[i][j] not in ['S', 'G']:
            new_grid[i][j] = '*'
    for row in new_grid:
        print(' '.join(row))

start = find_pos('S')
goal = find_pos('G')

# GBFS
start_time = time.time()
gbfs_path, gbfs_nodes = gbfs(start, goal)
gbfs_time = (time.time() - start_time) * 1000

# A*
start_time = time.time()
astar_path, astar_nodes = a_star(start, goal)
astar_time = (time.time() - start_time) * 1000

# Output
print("=== GBFS Path ===")
print_grid_path(terrain_grid, gbfs_path)
print(f"Visited Nodes: {gbfs_nodes}, Time: {gbfs_time:.3f} ms\n")

print("=== A* Path ===")
print_grid_path(terrain_grid, astar_path)
print(f"Visited Nodes: {astar_nodes}, Time: {astar_time:.3f} ms\n")

print("=== Comparison Summary ===")
print(f"A* {'lebih cepat' if astar_time < gbfs_time else 'lebih lambat'} dan {'lebih efisien' if astar_nodes < gbfs_nodes else 'kurang efisien'} dibandingkan GBFS.")
