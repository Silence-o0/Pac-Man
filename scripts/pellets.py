import pygame

from scripts.maze import CellTypes
from scripts.vector import Vector2
from scripts.constants import *
import numpy as np


class Pellet:
    def __init__(self, y_pos, x_pos):
        self.name = PELLET
        # self.position = Vector2(column * TILEWIDTH, row * TILEHEIGHT)
        self.cell_pos = (x_pos, y_pos)
        self.position = Vector2(x_pos * TILEWIDTH + LEFT_INDENT,
                         y_pos * TILEHEIGHT + TOP_INDENT)
        self.color = WHITE
        # self.radius = int(4 * TILEWIDTH / 16)
        # self.collideRadius = int(4 * TILEWIDTH / 16)
        self.radius = int(2 * TILEWIDTH / 16)
        self.collideRadius = int(2 * TILEWIDTH / 16)
        self.points = 10
        self.visible = True

    def render(self, surf):
        if self.visible:
            # pos = self.position.asInt()
            adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
            pos = self.position + adjust
            pygame.draw.circle(surf, self.color, pos.asInt(), self.radius)


# class PowerPellet(Pellet):
#     def __init__(self, row, column):
#         Pellet.__init__(self, row, column)
#         self.name = POWERPELLET
#         self.radius = int(8 * TILEWIDTH / 16)
#         self.points = 50
#         self.flashTime = 0.2
#         self.timer = 0
#
#     def update(self, dt):
#         self.timer += dt
#         if self.timer >= self.flashTime:
#             self.visible = not self.visible
#             self.timer = 0

class PelletGroup:
    def __init__(self, maze, home_point):
        self.pelletList = []
        # self.powerpellets = []
        self.createPelletList(maze, home_point)
        self.numEaten = 0
        self.quantity = 0

    def update(self, dt):
        pass
        # for powerpellet in self.powerpellets:
        #     powerpellet.update(dt)

    def createPelletList(self, maze, home_point):
        # data = self.readPelletfile(pelletfile)

        # for row in range(data.shape[0]):
        #     for col in range(data.shape[1]):
        #         if data[row][col] in ['.', '+']:
        #             self.pelletList.append(Pellet(row, col))
        #         elif data[row][col] in ['P', 'p']:
        #             pass
                    # pp = PowerPellet(row, col)
                    # self.pelletList.append(pp)
                    # self.powerpellets.append(pp)
        for row in range(NROWS):
            for col in range(NCOLS):
                if maze[col, row] == CellTypes.FREE and (col != home_point[0] or row != home_point[1]):
                    self.pelletList.append(Pellet(col, row))
                    # self.quantity += 1
                    # print(col, row)

    # def readPelletfile(self, textfile):
    #     return np.loadtxt(textfile, dtype='<U1')

    def isEmpty(self):
        if len(self.pelletList) == 0:
            return True
        return False

    def render(self, surf):
        for pellet in self.pelletList:
            pellet.render(surf)
