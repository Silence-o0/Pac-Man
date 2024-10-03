import pygame
from scripts.constants import *
from scripts.entity import Entity
from scripts.sprites import PacmanSprites


class Pacman(Entity):
    def __init__(self, x, y, grid):
        super().__init__(x, y, grid)
        self.sprites = PacmanSprites(self)
        self.speed = 70

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if self.alive:
            if keys[pygame.K_UP]:
                self.set_wait_direction('UP')
            elif keys[pygame.K_DOWN]:
                self.set_wait_direction('DOWN')
            elif keys[pygame.K_LEFT]:
                self.set_wait_direction('LEFT')
            elif keys[pygame.K_RIGHT]:
                self.set_wait_direction('RIGHT')

    def update(self, dt):
        if self.current_direction == "STOP" and self.wait_direction is not None:
            self.current_direction = self.wait_direction
            self.wait_direction = None
            self.set_move()

        if (self.x_pixels, self.y_pixels) != self.goal_point:
            diff = self.speed * dt
            if (abs(self.goal_point[0] - self.x_pixels) < diff + 0.5 and abs(self.goal_point[1] - self.y_pixels)
                    < diff + 0.5):
                self.x_pixels = self.goal_point[0]
                self.y_pixels = self.goal_point[1]
                self.x = self.goal_cell[0]
                self.y = self.goal_cell[1]
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
        self.current_direction = "STOP"
        self.sprites.reset()

    def reset(self):
        self.respawn()
        self.alive = True

    def get_current_cell(self, x_pix, y_pix):
        cell_x = int((x_pix-LEFT_INDENT) // TILEWIDTH)
        cell_y = int((y_pix-TOP_INDENT) // TILEHEIGHT)
        return cell_x, cell_y

    def eat_pellet(self, pelletList):
        for pellet in pelletList:
            if pellet.cell_pos == (self.x, self.y):
                return pellet
        return None
