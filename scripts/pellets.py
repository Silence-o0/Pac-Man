import pygame

from scripts.maze import CellTypes
from scripts.vector import Vector2
from scripts.constants import *


class Pellet:
    def __init__(self, y_pos, x_pos):
        self.name = PELLET
        self.cell_pos = (x_pos, y_pos)
        self.position = Vector2(x_pos * TILEWIDTH + LEFT_INDENT,
                         y_pos * TILEHEIGHT + TOP_INDENT)
        self.color = WHITE
        self.radius = int(2 * TILEWIDTH / 16)
        self.collideRadius = int(2 * TILEWIDTH / 16)
        self.points = 10
        self.visible = True

    def render(self, surf):
        if self.visible:
            adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
            pos = self.position + adjust
            pygame.draw.circle(surf, self.color, pos.asInt(), self.radius)


class PelletGroup:
    def __init__(self, maze, home_point):
        self.pelletList = []
        self.createPelletList(maze, home_point)
        self.numEaten = 0
        self.max_quantity = len(self.pelletList)

    def update(self, dt):
        pass

    def createPelletList(self, maze, home_point):
        for row in range(NROWS):
            for col in range(NCOLS):
                if maze[col, row] == CellTypes.FREE and (col != home_point[0] or row != home_point[1]):
                    self.pelletList.append(Pellet(col, row))

    def isEmpty(self):
        if len(self.pelletList) == 0:
            return True
        return False

    def render(self, surf):
        for pellet in self.pelletList:
            pellet.render(surf)
