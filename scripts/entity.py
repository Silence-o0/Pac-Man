from scripts.maze import CellTypes
from scripts.constants import *


class Entity:
    def __init__(self, x, y, grid):
        self.x = x    # column
        self.y = y    # row
        self.x_pixels = self.x * TILEWIDTH + LEFT_INDENT + PARTTILEWIDTH
        self.y_pixels = self.y * TILEHEIGHT + TOP_INDENT + PARTTILEHEIGHT
        self.grid = grid
        self.alive = True
        self.current_direction = "STOP"
        self.wait_direction = None
        self.speed = 0
        self.image = None
        self.goal_cell = (self.x, self.y)
        self.goal_point = (self.x_pixels, self.y_pixels)
        self.home_cell = (self.x, self.y)

    def respawn(self):
        self.current_direction = "STOP"
        self.x = self.home_cell[0]
        self.y = self.home_cell[1]
        self.x_pixels = self.x * TILEWIDTH + LEFT_INDENT + PARTTILEWIDTH
        self.y_pixels = self.y * TILEHEIGHT + TOP_INDENT + PARTTILEHEIGHT
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
            self.current_direction = "STOP"

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
        new_x = new_y = None

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

    def draw(self, screen):
        screen.blit(self.image, (self.x_pixels-PARTTILEWIDTH, self.y_pixels-PARTTILEHEIGHT))
