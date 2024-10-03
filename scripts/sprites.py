import pygame
from scripts.constants import *

from scripts.maze import CellTypes


class Spritesheet:
    def __init__(self):
        self.sheet = pygame.image.load("assets/spritesheet.png").convert()
        transcolor = self.sheet.get_at((0, 0))
        self.sheet.set_colorkey(transcolor)
        width = int(self.sheet.get_width() / (2*BASETILEWIDTH) * TILEWIDTH)
        height = int(self.sheet.get_height() / (2*BASETILEHEIGHT) * TILEHEIGHT)
        self.sheet = pygame.transform.scale(self.sheet, (width, height))

    def getImage(self, x, y, width, height):
        x *= TILEWIDTH
        y *= TILEHEIGHT
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())


class PacmanSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.entity = entity
        self.entity.image = self.getStartImage()
        self.animations = {}
        self.defineAnimations()
        self.stopimage = (8, 0)

    def getStartImage(self):
        return self.getImage(0, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, TILEWIDTH, TILEHEIGHT)

    def defineAnimations(self):
        pass

    def update(self, dt):
        if self.entity.alive:
            if self.entity.current_direction == 'LEFT':
                self.entity.image = self.getImage(0, 0)
                self.stopimage = (8, 0)
            elif self.entity.current_direction == 'RIGHT':
                self.entity.image = self.getImage(1, 0)
                self.stopimage = (10, 0)
            elif self.entity.current_direction == 'DOWN':
                self.entity.image = self.getImage(2, 0)
                self.stopimage = (8, 2)
            elif self.entity.current_direction == 'UP':
                self.entity.image = self.getImage(3, 0)
                self.stopimage = (10, 2)
            elif self.entity.current_direction == 'STOP':
                pass
        else:
            self.entity.image = self.getImage(5, 0)

    def reset(self):
        for key in list(self.animations.keys()):
            self.animations[key].reset()


class GhostSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.x = {BLINKY: 0, PINKY: 1, INKY: 2, CLYDE: 2}
        self.entity = entity
        self.entity.image = self.getStartImage()

    def getStartImage(self):
        return self.getImage(self.x[self.entity.name], 4)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, TILEWIDTH, TILEHEIGHT)

    def update(self, dt):
        x = self.x[self.entity.name]
        if self.entity.current_direction == 'LEFT':
            self.entity.image = self.getImage(x, 4)
        elif self.entity.current_direction == 'RIGHT':
            self.entity.image = self.getImage(x, 5)
        elif self.entity.current_direction == 'DOWN':
            self.entity.image = self.getImage(x, 3)
        elif self.entity.current_direction == 'UP':
            self.entity.image = self.getImage(x, 2)


class LifeSprites(Spritesheet):
    def __init__(self, num_lives):
        Spritesheet.__init__(self)
        self.resetLives(num_lives)

    def removeImage(self):
        if len(self.images) > 0:
            self.images.pop(0)

    def resetLives(self, num_lives):
        self.images = []
        for i in range(num_lives):
            self.images.append(self.getImage(0, 0))

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, TILEWIDTH, TILEHEIGHT)


class MazeSprites(Spritesheet):
    def __init__(self, maze):
        Spritesheet.__init__(self)
        self.data = maze

    def constructBackground(self, background):
        for row in list(range(self.data.rows)):
            for col in list(range(self.data.cols)):
                if self.data[row, col] == CellTypes.HOUSE:
                    pygame.draw.rect(background, HOUSE_COLOR,
                                     pygame.Rect(col * TILEWIDTH + LEFT_INDENT, row * TILEHEIGHT + TOP_INDENT, TILEWIDTH, TILEHEIGHT))
                elif self.data[row, col] == CellTypes.FREE:
                    pygame.draw.rect(background, PATH_COLOR,
                                     pygame.Rect(col * TILEWIDTH + LEFT_INDENT, row * TILEHEIGHT + TOP_INDENT, TILEWIDTH, TILEHEIGHT))
                else:
                    pygame.draw.rect(background, WALL_COLOR,
                                     pygame.Rect(col * TILEWIDTH + LEFT_INDENT, row * TILEHEIGHT + TOP_INDENT, TILEWIDTH, TILEHEIGHT))
        return background
