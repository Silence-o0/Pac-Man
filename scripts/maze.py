import enum
import itertools

import pygame
import numpy as np
from scripts.vector import Vector2
from scripts.constants import *

from collections.abc import MutableMapping


class CellTypes(enum.Enum):
    FREE = enum.auto()
    WALL = enum.auto()
    HOUSE = enum.auto()


class Maze(MutableMapping):
    def __init__(self):
        self.rows = NROWS
        self.cols = NCOLS
        self.maze = [
            [CellTypes.WALL, CellTypes.WALL, CellTypes.WALL, CellTypes.WALL, CellTypes.WALL, CellTypes.WALL,
             CellTypes.WALL, CellTypes.WALL, CellTypes.WALL, CellTypes.WALL, CellTypes.WALL],
            [CellTypes.WALL, CellTypes.FREE, CellTypes.FREE, CellTypes.FREE, CellTypes.FREE, CellTypes.WALL,
             CellTypes.FREE, CellTypes.FREE, CellTypes.FREE, CellTypes.FREE, CellTypes.WALL],
            [CellTypes.WALL, CellTypes.FREE, CellTypes.WALL, CellTypes.WALL, CellTypes.FREE, CellTypes.FREE,
             CellTypes.FREE, CellTypes.WALL, CellTypes.WALL, CellTypes.FREE, CellTypes.WALL],
            [CellTypes.WALL, CellTypes.FREE, CellTypes.WALL, CellTypes.FREE, CellTypes.FREE, CellTypes.WALL,
             CellTypes.FREE, CellTypes.FREE, CellTypes.WALL, CellTypes.FREE, CellTypes.WALL],
            [CellTypes.WALL, CellTypes.FREE, CellTypes.WALL, CellTypes.FREE, CellTypes.WALL, CellTypes.WALL,
             CellTypes.WALL, CellTypes.FREE, CellTypes.WALL, CellTypes.FREE, CellTypes.WALL],
            [CellTypes.WALL, CellTypes.FREE, CellTypes.FREE, CellTypes.FREE, CellTypes.FREE, CellTypes.FREE,
             CellTypes.FREE, CellTypes.FREE, CellTypes.FREE, CellTypes.FREE, CellTypes.WALL],

            [CellTypes.WALL, CellTypes.WALL, CellTypes.FREE, CellTypes.WALL, CellTypes.HOUSE, CellTypes.HOUSE,
             CellTypes.HOUSE, CellTypes.WALL, CellTypes.FREE, CellTypes.WALL, CellTypes.WALL],

            [CellTypes.WALL, CellTypes.FREE, CellTypes.FREE, CellTypes.WALL, CellTypes.WALL, CellTypes.WALL,
             CellTypes.WALL, CellTypes.WALL, CellTypes.FREE, CellTypes.FREE, CellTypes.WALL],
            [CellTypes.WALL, CellTypes.FREE, CellTypes.WALL, CellTypes.WALL, CellTypes.FREE, CellTypes.FREE,
             CellTypes.FREE, CellTypes.WALL, CellTypes.WALL, CellTypes.FREE, CellTypes.WALL],
            [CellTypes.WALL, CellTypes.FREE, CellTypes.FREE, CellTypes.FREE, CellTypes.FREE, CellTypes.WALL,
             CellTypes.FREE, CellTypes.FREE, CellTypes.FREE, CellTypes.FREE, CellTypes.WALL],
            [CellTypes.WALL, CellTypes.WALL, CellTypes.WALL, CellTypes.WALL, CellTypes.WALL, CellTypes.WALL,
             CellTypes.WALL, CellTypes.WALL, CellTypes.WALL, CellTypes.WALL, CellTypes.WALL],
        ]

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


# maze = Maze()
# maze[1 ,2]
#
#
# del maze[1, 1]
# maze.__getitem__((1, 1))
# maze.maze[1][1]
#
# for (x, y), value in maze.items():
#     pass
