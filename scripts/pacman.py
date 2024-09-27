import math

import pygame
from pygame.locals import *

from scripts.maze import CellTypes
from scripts.vector import Vector2
from scripts.constants import *
from scripts.entity import Entity
from scripts.sprites import PacmanSprites


class Pacman(Entity):
    def __init__(self, x, y, grid):
        # self.x_pixels = x * TILEWIDTH + LEFT_INDENT + 16  # Початкова позиція по X в пікселях
        # self.y_pixels = y * TILEHEIGHT + TOP_INDENT + 16  # Початкова позиція по Y в пікселях
        super().__init__(x, y, grid)
        self.sprites = PacmanSprites(self)  # Ініціалізуємо анімацію Пакмена
        self.speed = 100

    # def move_up(self):
    #     self.move(0, -1)
    #     self.direction = 'UP'
    #
    # def move_down(self):
    #     self.move(0, 1)
    #     self.direction = 'DOWN'
    #
    # def move_left(self):
    #     self.move(-1, 0)
    #     self.direction = 'LEFT'
    #
    # def move_right(self):
    #     self.move(1, 0)
    #     self.direction = 'RIGHT'

    def set_move(self):
        if self.current_direction == "LEFT":
            self.move(-1, 0)
        elif self.current_direction == "RIGHT":
            self.move(1, 0)
        elif self.current_direction == "UP":
            self.move(0, -1)
        elif self.current_direction == "DOWN":
            self.move(0, 1)

    def set_wait_direction(self, direction):
        current_x = self.goal_cell[0]
        current_y = self.goal_cell[1]

        if direction == "LEFT":
            new_x = current_x - 1
            new_y = current_y
        elif direction == "RIGHT":
            new_x = current_x + 1
            new_y = current_y
        elif direction == "UP":
            new_y = current_y - 1
            new_x = current_x
        elif direction == "DOWN":
            new_y = current_y + 1
            new_x = current_x

        if (new_x > 0 and new_x < NCOLS) and (new_y > 0 and new_y < NROWS):
            if self.grid[new_y, new_x] == CellTypes.FREE:
                self.wait_direction = direction
                if self.current_direction == "STOP":
                    self.current_direction = self.wait_direction

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if True:
        # if (((self.x_pixels-PARTTILEWIDTH)-LEFT_INDENT) % TILEWIDTH == 0) and (((self.y_pixels-PARTTILEHEIGHT)-TOP_INDENT) % TILEHEIGHT == 0):
            if keys[pygame.K_UP]:
                # self.direction = 'UP'
                self.set_wait_direction('UP')
            elif keys[pygame.K_DOWN]:
                # self.direction = 'DOWN'
                self.set_wait_direction('DOWN')
            elif keys[pygame.K_LEFT]:
                # self.direction = 'LEFT'
                self.set_wait_direction('LEFT')
            elif keys[pygame.K_RIGHT]:
                # self.direction = 'RIGHT'
                self.set_wait_direction('RIGHT')


    def update(self, dt):
        # print("CurDir:", self.current_direction)
        # print("WaitDir:", self.wait_direction)
        # print("Cell:", self.x, self.y)
        # print("GoalCell:", self.goal_cell[0], self.goal_cell[1])
        # print("Pixels:", self.x_pixels, self.y_pixels)
        # print("GoalPixels:", self.goal_point[0], self.goal_point[1])

        if self.current_direction == 0 and self.wait_direction is not None:
            self.current_direction = self.wait_direction
            self.wait_direction = None
            self.set_move()

        if (self.x_pixels, self.y_pixels) != self.goal_point:
            diff = self.speed * dt
            if abs(self.goal_point[0] - self.x_pixels) < diff + 0.5 and abs(self.goal_point[1] - self.y_pixels) < diff + 0.5:
                self.x_pixels = self.goal_point[0]
                self.y_pixels = self.goal_point[1]
                self.x = self.goal_cell[0]
                self.y = self.goal_cell[1]
                # self.eat_pellet()
                if self.wait_direction is not None:
                    self.current_direction = self.wait_direction
                    self.wait_direction = None
                    self.set_move()
                else:
                    self.set_move()
            else:
                x_displace = self.goal_cell[0] - self.x
                y_displace = self.goal_cell[1] - self.y

                self.x_pixels = self.x_pixels + (self.speed * dt) * x_displace
                self.y_pixels = self.y_pixels + (self.speed * dt) * y_displace

        self.sprites.update(dt)

    def die(self):
        self.alive = False
        self.direction = 'STOP'
        self.sprites.reset()  # Скидаємо анімацію

    def pause(self):
        self.direction = 'STOP'

    def respawn(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.sprites.reset()  # Скидаємо анімацію

    def get_current_cell(self, x_pix, y_pix):
        cell_x = int((x_pix-LEFT_INDENT) // TILEWIDTH)  # Індекс по X
        cell_y = int((y_pix-TOP_INDENT) // TILEHEIGHT)  # Індекс по Y
        return cell_x, cell_y

    def eat_pellet(self, pelletList):
        for pellet in pelletList:
            if pellet.cell_pos == (self.x, self.y):
                return pellet
        return None


# class Pacman(Entity):
    # def __init__(self, node):
    #     Entity.__init__(self, node)
    # def __init__(self, home_point):
    #     Entity.__init__(self, home_point)
    #     self.name = PACMAN
    #     self.color = YELLOW
    #     self.direction = LEFT
        # self.setBetweenNodes(LEFT)
        # self.position = home_point
        # self.alive = True
        # self.sprites = PacmanSprites(self)
        # self.last_dir = STOP

    # def reset(self):
    #     Entity.reset(self)
    #     self.direction = LEFT
    #     self.setBetweenNodes(LEFT)
    #     self.alive = True
    #     self.image = self.sprites.getStartImage()
    #     self.sprites.reset()
    #     self.last_dir = STOP

    # def die(self):
    #     self.alive = False
    #     self.direction = STOP
    #
    # def update(self, dt):
    #     self.sprites.update(dt)
    #     self.position += self.directions[self.direction] * self.speed * dt
    #     direction = self.getValidKey()
    #
    #     if direction != STOP:
    #         self.last_dir = direction

        # next_node = None
        # if self.direction != STOP:
        #     if self.node.neighbors[self.direction] != None:
        #         next_node = self.node.neighbors[self.direction]
        #
        #
        # if next_node != None and self.last_dir != STOP:
        #     print(self.validDirectionOfNode(self.last_dir, next_node))
            # if self.validDirectionOfNode(self.last_dir, next_node) == True and self.overshotNode(next_node):
            #     self.node = next_node
            #     self.direction = self.last_dir
            #     last_dir = STOP
        #
        #
        # if self.overshotTarget():
        #     self.node = self.target
        #     if self.node.neighbors[PORTAL] is not None:
        #         self.node = self.node.neighbors[PORTAL]
        #     self.target = self.getNewTarget(direction)
        #     if self.target is not self.node:
        #         self.direction = direction
        #     else:
        #         self.target = self.getNewTarget(self.direction)
        #
        #     if self.target is self.node:
        #         self.direction = STOP

            # self.setPosition()

        # else:
        #     if self.oppositeDirection(direction):
        #         self.reverseDirection()
    #
    # def eatPellets(self, pelletList):
    #     for pellet in pelletList:
    #         if self.collideCheck(pellet):
    #             return pellet
    #     return None
    #
    # def collideGhost(self, ghost):
    #     return self.collideCheck(ghost)
    #
    # def collideCheck(self, other):
    #     dist = self.position - other.position
    #     distSquared = dist.magnitudeSquared()
    #     radSquared = (self.collideRadius + other.collideRadius) ** 2
    #     if distSquared <= radSquared:
    #         return True
    #     return False

    # def getValidKey(self):
    #     key_pressed = pygame.key.get_pressed()
    #     if key_pressed[K_UP]:
    #         return UP
    #     if key_pressed[K_DOWN]:
    #         return DOWN
    #     if key_pressed[K_LEFT]:
    #         return LEFT
    #     if key_pressed[K_RIGHT]:
    #         return RIGHT
    #     return STOP
