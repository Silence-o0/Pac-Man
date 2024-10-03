import random

from scripts.constants import *
from scripts.maze import CellTypes


class DirectionMethods:
    @staticmethod
    def random_move(ghost, grid):
        current_direction = ghost.current_direction
        x, y = ghost.x, ghost.y

        neighbors = {
            "LEFT": (x - 1, y),
            "RIGHT": (x + 1, y),
            "UP": (x, y - 1),
            "DOWN": (x, y + 1)
        }

        valid_directions = [direction for direction, (nx, ny) in neighbors.items()
                            if 0 <= nx < NCOLS and 0 <= ny < NROWS and grid[ny, nx] == CellTypes.FREE]
        if not valid_directions:
            return current_direction

        next_cell = neighbors.get(current_direction)
        if next_cell and grid[next_cell[1], next_cell[0]] == CellTypes.FREE:
            if len(valid_directions) == 2 and current_direction in valid_directions:
                return current_direction

        opposite_direction = {
            "LEFT": "RIGHT",
            "RIGHT": "LEFT",
            "UP": "DOWN",
            "DOWN": "UP"
        }
        backward_direction = opposite_direction.get(current_direction)

        weighted_directions = []
        for direction in valid_directions:
            if direction == backward_direction:
                weighted_directions += [direction] * 1
            else:
                weighted_directions += [direction] * 3

        new_direction = random.choice(weighted_directions)
        return new_direction

    @staticmethod
    def bfs_to_pacman(ghost, grid, pacman, visited=None):
        if visited is None:
            visited = set()
        ghost_position = (ghost.x, ghost.y)
        pacman_position = (pacman.x, pacman.y)

        if ghost_position != pacman_position:
            queue = [(ghost_position, None)]
            visited.add(ghost_position)

            directions = {
                "LEFT": (-1, 0),
                "RIGHT": (1, 0),
                "UP": (0, -1),
                "DOWN": (0, 1)
            }

            while queue:
                (current_position, first_direction) = queue.pop(0)
                x, y = current_position

                for direction, (dx, dy) in directions.items():
                    nx, ny = x + dx, y + dy
                    next_position = (nx, ny)

                    if (0 <= nx < NCOLS and 0 <= ny < NROWS and grid[ny, nx] == CellTypes.FREE
                            and next_position not in visited):
                        if next_position == pacman_position:
                            return first_direction or direction
                        queue.append((next_position, first_direction or direction))
                        visited.add(next_position)
        return None
