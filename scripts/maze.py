import enum
import itertools
import random
from collections import deque, defaultdict
from scripts.constants import *
from collections.abc import MutableMapping


class CellTypes(enum.Enum):
    FREE = enum.auto()
    WALL = enum.auto()
    HOUSE = enum.auto()


class Directions(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()


class Maze(MutableMapping):
    def __init__(self, level):
        self.rows = NROWS
        self.cols = NCOLS
        self.max_crossroads = self.get_max_crossroads(level)
        self.maze = self.maze_generate()

    def __iter__(self):
        return itertools.product(range(self.rows), range(self.cols))

    def __len__(self):
        pass

    def __getitem__(self, key):
        return self.maze[key[0]][key[1]]

    def __delitem__(self, key):
        self.maze[key[0]][key[1]] = 0

    def __setitem__(self, key, __value):
        pass

    def render(self):
        for (x, y), value in self.items():
            pass

    def get_max_crossroads(self, level):
        if level >= 5:
            diff = level - 4
            return 30-diff
        return None

    def generate_map(self, vtiles: int, htiles: int) -> list[str]:
        crossroads_count = 0
        spawn_r, spawn_c = spawn_coord = (vtiles // 2, htiles // 2)

        tiles: defaultdict[tuple[int, int], set[Directions]] = defaultdict(set)
        tiles[spawn_coord] = {Directions.UP, Directions.RIGHT, Directions.LEFT}

        queue = deque([(spawn_r - 1, spawn_c), (spawn_r, spawn_c - 1),
                       (spawn_r, spawn_c + 1)])
        while queue:
            cur_r, cur_c = cur_coord = queue.popleft()
            if cur_coord in tiles:
                continue

            all_moves = [
                (Directions.UP, (-1, 0), Directions.DOWN),
                (Directions.DOWN, (1, 0), Directions.UP),
                (Directions.LEFT, (0, -1), Directions.RIGHT),
                (Directions.RIGHT, (0, 1), Directions.LEFT),
            ]
            required_dirs = []
            possible_dirs = []
            last_resort_dirs = []
            for this_tile_dir, (r_offset, c_offset), other_tile_dir in all_moves:
                next_r = cur_r + r_offset
                next_c = cur_c + c_offset
                next_coord = (next_r, next_c)

                if not 0 <= next_r < vtiles or not 0 <= next_c < htiles:
                    continue

                if next_coord not in tiles:
                    possible_dirs.append((this_tile_dir, next_coord))
                elif other_tile_dir in tiles[next_coord]:
                    required_dirs.append(this_tile_dir)
                elif next_coord != spawn_coord:
                    last_resort_dirs.append((this_tile_dir, next_coord, other_tile_dir))

            dirs_still_needed = max(2 - len(required_dirs), 0)

            if len(possible_dirs) < dirs_still_needed:
                additional_dirs = possible_dirs
                last_resort_dirs = random.sample(
                    last_resort_dirs, dirs_still_needed - len(possible_dirs)
                )
            else:
                additional_dirs_n = dirs_still_needed
                if not self.max_crossroads or crossroads_count < self.max_crossroads:
                    additional_dirs_n = random.randint(dirs_still_needed, len(possible_dirs))
                additional_dirs = random.sample(possible_dirs, additional_dirs_n)
                last_resort_dirs = []

            tiles[cur_coord] = set(required_dirs)
            for dir, next_coord in additional_dirs:
                tiles[cur_coord].add(dir)
                queue.append(next_coord)

            for dir, next_coord, other_tile_dir in last_resort_dirs:
                tiles[cur_coord].add(dir)
                tiles[next_coord].add(other_tile_dir)

            if (len(tiles[cur_coord])+len(last_resort_dirs)) > 2:
                crossroads_count += 1

        return self.convert_tiles_to_str_map(vtiles, htiles, tiles, spawn_coord)

    def convert_tiles_to_str_map(self,
                                 vtiles: int,
                                 htiles: int,
                                 tiles: dict[tuple[int, int], set[Directions]],
                                 spawn_coord: tuple[int, int],
                                 ) -> list[str]:
        str_map: list[str] = []
        for r in range(vtiles):
            row = ''
            for c in range(htiles):
                if Directions.UP in tiles[r, c]:
                    row += '#.#'
                else:
                    row += '###'
            str_map.append(row)

            row = ''
            for c in range(htiles):
                if (r, c) == spawn_coord:
                    row += '...'
                    continue

                tile = tiles[r, c]
                row += '.' if Directions.LEFT in tile else '#'
                row += '.' if tile else '#'
                row += '.' if Directions.RIGHT in tile else '#'
            str_map.append(row)

            row = ''
            for c in range(htiles):
                if (r, c) == spawn_coord:
                    row += '&&&'
                    continue
                if Directions.DOWN in tiles[r, c]:
                    row += '#.#'
                else:
                    row += '###'
            str_map.append(row)
        return str_map

    def check_min_path(self, current_str_map):
        path_quantity = 0
        for row in current_str_map:
            path_quantity += row.count('.')
        if path_quantity > 0.15 * (NCOLS * NROWS):
            return True
        return False

    def maze_generate(self):
        def maze_fill(tile_map):
            def set_cell(row_index, col_index, symb):
                try:
                    cell_type = CellTypes(symb)
                except ValueError:
                    cell_type = None
                maze[row_index][col_index] = cell_type

            for row_index, row in enumerate(tile_map):
                for col_index, symb in enumerate(row):
                    set_cell(row_index, col_index, symb)

        maze = [[None for _ in range(self.rows)] for _ in range(self.cols)]
        str_map = self.generate_map(self.rows // 3, self.cols // 3)

        while not self.check_min_path(str_map):
            str_map = self.generate_map(self.rows // 3, self.cols // 3)
        maze_fill(str_map)

        return maze
