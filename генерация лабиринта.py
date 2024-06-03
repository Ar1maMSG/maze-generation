import matplotlib.pyplot as plt
from random import randint, choice
from dataclasses import dataclass, field


@dataclass
class MazeCell:
    x: int
    y: int
    component: int
    is_open: bool = field(default=False)
    walls: list = field(default_factory=lambda: [True, True, True, True])  # Top, Right, Bottom, Left


N = 30
LINE_WIDTH = 2


class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1


def generate_maze(size) -> list:
    maze = [[MazeCell(x, y, x * size + y) for y in range(size)] for x in range(size)]
    uf = UnionFind(size * size)

    directions = [(-1, 0, 0, 2), (1, 0, 2, 0), (0, -1, 3, 1), (0, 1, 1, 3)]

    while uf.find(0) != uf.find(size * size - 1):
        x, y = randint(0, size - 1), randint(0, size - 1)
        dx, dy, wall, opp_wall = choice(directions)
        nx, ny = x + dx, y + dy
        if 0 <= nx < size and 0 <= ny < size:
            if uf.find(x * size + y) != uf.find(nx * size + ny):
                uf.union(x * size + y, nx * size + ny)
                maze[x][y].walls[wall] = False
                maze[nx][ny].walls[opp_wall] = False

    maze[0][0].is_open = True
    maze[size - 1][size - 1].is_open = True
    return maze


def draw_maze(maze):
    size = len(maze)
    fig, ax = plt.subplots(figsize=(10, 10))
    for x in range(size):
        for y in range(size):
            cell = maze[x][y]
            if cell.walls[0]:
                ax.plot([y, y + 1], [size - x, size - x], 'k-', lw=LINE_WIDTH)  # Top
            if cell.walls[1]:
                ax.plot([y + 1, y + 1], [size - x, size - x - 1], 'k-', lw=LINE_WIDTH)  # Right
            if cell.walls[2]:
                ax.plot([y, y + 1], [size - x - 1, size - x - 1], 'k-', lw=LINE_WIDTH)  # Bottom
            if cell.walls[3]:
                ax.plot([y, y], [size - x, size - x - 1], 'k-', lw=LINE_WIDTH)  # Left

    ax.axis('off')
    plt.show()


# Generate and draw the maze
maze = generate_maze(N)
draw_maze(maze)
