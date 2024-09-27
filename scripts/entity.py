import pygame
from pygame.locals import *

from scripts.maze import CellTypes
from scripts.vector import Vector2
from scripts.constants import *
from random import randint


class Entity:
    def __init__(self, x, y, grid):
        self.x = x    # column
        self.y = y    # row
        self.x_pixels = self.x * TILEWIDTH + LEFT_INDENT + PARTTILEWIDTH
        self.y_pixels = self.y * TILEHEIGHT + TOP_INDENT + PARTTILEHEIGHT
        self.grid = grid
        self.alive = True
        self.current_direction = STOP
        self.wait_direction = None
        self.speed = 0
        self.image = None  # Зображення завантажується пізніше через PacmanSprites
        self.goal_cell = (self.x, self.y)
        self.goal_point = (self.x_pixels, self.y_pixels)

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < NCOLS and 0 <= new_y < NROWS and self.grid[new_y, new_x] == CellTypes.FREE:
            self.goal_cell = (new_x, new_y)
            self.goal_point = (new_x * TILEWIDTH + LEFT_INDENT + PARTTILEWIDTH,
                               new_y * TILEHEIGHT + TOP_INDENT + PARTTILEHEIGHT)
        else:
            self.current_direction = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x_pixels-PARTTILEWIDTH, self.y_pixels-PARTTILEHEIGHT))



# class Entity:
    # def __init__(self, home_point):
    #     self.name = None
    #     self.directions = {STOP: Vector2(), UP: Vector2(0, -1), DOWN: Vector2(0, 1), LEFT: Vector2(-1, 0),
    #                        RIGHT: Vector2(1, 0)}
    #     self.direction = STOP
    #     self.setSpeed(100)
    #     self.radius = 10
    #     self.collideRadius = 5
    #     self.color = WHITE
    #     self.node = node
        # self.setPosition()
        # self.position = None
        # self.target = None
        # self.visible = True
        # self.disablePortal = False
        # self.goal = None
        # self.startPoint = home_point
        # self.directionMethod = self.randomDirection
        # self.image = None

    # def setBetweenNodes(self, direction):
    #     if self.node.neighbors[direction] is not None:
    #         self.target = self.node.neighbors[direction]
    #         self.position = (self.node.position + self.target.position) / 2.0

    # def setStartNode(self, node):
    #     self.node = node
    #     self.startNode = node
    #     self.target = node
    #     self.setPosition()

    # def reset(self):
    #     self.setStartNode(self.startNode)
    #     self.direction = STOP
    #     self.speed = 100
    #     self.visible = True

    # def update(self, dt):
    #     self.position += self.directions[self.direction] * self.speed * dt

        # if self.overshotTarget():
        #     self.node = self.target
        #     directions = self.validDirections()
            # direction = self.directionMethod(directions)
            # if not self.disablePortal:
            #     if self.node.neighbors[PORTAL] is not None:
            #         self.node = self.node.neighbors[PORTAL]
            # self.target = self.getNewTarget(direction)
            # if self.target is not self.node:
            #     self.direction = direction
            # else:
            #     self.target = self.getNewTarget(self.direction)
            #
            # self.setPosition()

    # def validDirections(self):
    #     directions = []
    #     for key in [UP, DOWN, LEFT, RIGHT]:
    #         if self.validDirection(key):
    #             if key != self.direction * -1:
    #                 directions.append(key)
    #     if len(directions) == 0:
    #         directions.append(self.direction * -1)
    #     return directions

    # def randomDirection(self, directions):
    #     return directions[randint(0, len(directions) - 1)]
    #
    # def setPosition(self):
    #     self.position = self.node.position.copy()
    #
    # def validDirection(self, direction):
    #     if direction is not STOP:
    #         if self.name in self.node.access[direction]:
    #             if self.node.neighbors[direction] is not None:
    #                 return True
    #     return False

    # def validDirectionOfNode(self, direction, node):
    #     if direction is not STOP:
    #         if self.name in self.node.access[direction]:
    #             if node.neighbors[direction] is not None:
    #                 return True
    #     return False
    #
    # def getNewTarget(self, direction):
    #     if self.validDirection(direction):
    #         return self.node.neighbors[direction]
    #     return self.node
    #
    # def overshotNode(self, node):
    #     if self.node is not None:
    #         vec1 = node.position - self.node.position
    #         vec2 = self.position - self.node.position
    #         node2Target = vec1.magnitudeSquared()
    #         node2Self = vec2.magnitudeSquared()
    #         return node2Self >= node2Target
    #     return False
    #
    # def overshotTarget(self):
    #     if self.target is not None:
    #         vec1 = self.target.position - self.node.position
    #         vec2 = self.position - self.node.position
    #         node2Target = vec1.magnitudeSquared()
    #         node2Self = vec2.magnitudeSquared()
    #         return node2Self >= node2Target
    #     return False
    #
    # def reverseDirection(self):
    #     self.direction *= -1
    #     aux = self.node
    #     self.node = self.target
    #     self.target = aux
    #
    # def oppositeDirection(self, direction):
    #     if direction is not STOP and direction == self.direction * -1:
    #         return True
    #     return False
    #
    # def setSpeed(self, speed):
    #     self.speed = speed * TILEWIDTH / 16

    # def goalDirection(self, directions):
    #     distances = []
    #     for direction in directions:
    #         vec = self.node.position + self.directions[direction] * TILEWIDTH - self.goal
    #         distances.append(vec.magnitudeSquared())
    #     index = distances.index(min(distances))
    #     return directions[index]
    #


    # def render(self, surf):
    #     if self.visible:
    #         if self.image is not None:
    #             adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
    #             pos = self.position - adjust
    #             surf.blit(self.image, pos.asTuple())
    #             surf.blit(self.image, self.position.asTuple())
            # else:
            #     pos = self.position.asInt()
            #     pygame.draw.circle(surf, self.color, pos, self.radius)
#