import pygame
from scripts.vector import Vector2
from scripts.constants import *


class Text:
    def __init__(self, text, color, x, y, size, time=None, id=None, visible=True):
        self.id = id
        self.text = text
        self.color = color
        self.size = size
        self.visible = visible
        self.position = Vector2(x, y)
        self.timer = 0
        self.lifespan = time
        self.label = None
        self.destroy = False
        self.setupFont("assets/fonts/Nexa-Heavy.ttf")
        self.createLabel()

    def setupFont(self, fontpath):
        self.font = pygame.font.Font(fontpath, self.size)

    def createLabel(self):
        self.label = self.font.render(self.text, 1, self.color)

    def setText(self, newtext):
        self.text = str(newtext)
        self.createLabel()

    def update(self, dt):
        if self.lifespan is not None:
            self.timer += dt
            if self.timer >= self.lifespan:
                self.timer = 0
                self.lifespan = None
                self.destroy = True

    def render(self, screen):
        if self.visible:
            x, y = self.position.asTuple()
            screen.blit(self.label, (x, y))


class TextGroup(object):
    def __init__(self):
        self.nextid = 10
        self.alltext = {}
        self.setupText()
        self.showText(READYTXT)

    def addText(self, text, color, x, y, size, time=None, id=None):
        self.nextid += 1
        self.alltext[self.nextid] = Text(text, color, x, y, size, time=time, id=id)
        return self.nextid

    def removeText(self, id):
        self.alltext.pop(id)

    def setupText(self):
        size = TOP_INDENT // 4
        self.alltext[SCORETXT] = Text("0".zfill(8), WHITE, 0, TILEHEIGHT//2, size)
        self.alltext[LEVELTXT] = Text(str(1).zfill(3), WHITE, LEFT_INDENT + NCOLS * TILEWIDTH, TILEHEIGHT//2, size)
        self.alltext[READYTXT] = Text("READY!", YELLOW, 10 * TILEWIDTH, 8 * TILEHEIGHT, 4 * size, visible=False)
        self.alltext[PAUSETXT] = Text("PAUSED!", YELLOW, 9.5 * TILEWIDTH, 8 * TILEHEIGHT, 4 * size, visible=False)
        self.alltext[GAMEOVERTXT] = Text("GAMEOVER!", YELLOW, 8 * TILEWIDTH, 8 * TILEHEIGHT, 4 * size, visible=False)
        self.addText("SCORE", WHITE, 0, 0, size)
        self.addText("LEVEL", WHITE, LEFT_INDENT + NCOLS * TILEWIDTH, 0, size)

    def update(self, dt):
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].update(dt)
            if self.alltext[tkey].destroy:
                self.removeText(tkey)

    def showText(self, name):
        self.hideText()
        self.alltext[name].visible = True

    def hideText(self):
        self.alltext[READYTXT].visible = False
        self.alltext[PAUSETXT].visible = False
        self.alltext[GAMEOVERTXT].visible = False

    def updateScore(self, score):
        self.updateText(SCORETXT, str(score).zfill(8))

    def updateLevel(self, level):
        self.updateText(LEVELTXT, str(level + 1).zfill(3))

    def updateText(self, name, value):
        if name in self.alltext.keys():
            self.alltext[name].setText(value)

    def render(self, screen):
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].render(screen)
