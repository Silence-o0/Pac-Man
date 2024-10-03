import pygame

from pygame.locals import *
from scripts.constants import *
from scripts.pacman import Pacman
from scripts.pellets import PelletGroup
from scripts.ghosts import Ghost
from scripts.maze import Maze
from scripts.pauser import Pause
from scripts.text import TextGroup
from scripts.sprites import LifeSprites
from scripts.sprites import MazeSprites


class GameController:
    def __init__(self):
        self.pellets = None
        self.pacman = None
        self.ghosts = []
        pygame.init()
        pygame.display.set_caption('PacMan')
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.background_norm = None
        self.background_flash = None
        self.clock = pygame.time.Clock()
        self.pause = Pause(True)
        self.level = 0
        self.lives = 5
        self.score = 0
        self.textgroup = TextGroup()
        self.lifesprites = LifeSprites(self.lives)
        self.flashBG = False
        self.flashTime = 0.2
        self.flashTimer = 0
        self.fruitCaptured = []

    def restartGame(self):
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.pause.timer = 0
        self.ghosts = []
        self.startGame()
        self.score = 0
        self.textgroup.updateScore(self.score)
        self.textgroup.updateLevel(self.level)
        self.textgroup.showText(READYTXT)
        self.lifesprites.resetLives(self.lives)

    def resetLevel(self):
        self.pause.paused = True
        self.pause.timer = 0
        self.pacman.reset()
        for ghost in self.ghosts:
            ghost.respawn()
        self.textgroup.showText(READYTXT)

    def nextLevel(self):
        self.ghosts = []
        self.pause.timer = 0
        self.level += 1
        self.pause.paused = True
        self.startGame()
        self.textgroup.updateLevel(self.level)

    def startGame(self):
        maze = Maze(self.level)
        self.mazesprites = MazeSprites(maze)
        self.setBackground()
        central_tile = (NCOLS//6, NROWS//6)
        pacman_homepoint = ((central_tile[0]*3)+1, (central_tile[1]*3)+1)
        ghosts_homepoint = ((central_tile[0]*3)+1, (central_tile[1]*3)+2)

        self.pacman = Pacman(pacman_homepoint[0], pacman_homepoint[1], maze)
        self.pellets = PelletGroup(maze, pacman_homepoint)

        ghost = Ghost(ghosts_homepoint, maze, self.pacman, PINKY, 3)
        self.ghosts.append(ghost)

        self.pacman.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw(self.screen)

    def setBackground(self):
        self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_norm.fill(BLACK)
        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_flash.fill(BLACK)
        self.background_norm = self.mazesprites.constructBackground(self.background_norm)
        self.background_flash = self.mazesprites.constructBackground(self.background_flash)
        self.flashBG = False
        self.background = self.background_norm

    def updateScore(self, points):
        self.score += points
        self.textgroup.updateScore(self.score)

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.textgroup.update(dt)
        self.pacman.handle_input()

        if self.pacman.alive:
            if not self.pause.paused:
                for ghost in self.ghosts:
                    if self.pause.timer > ghost.start_time:
                        ghost.update(dt)
                self.checkPelletEvents()
                self.checkGhostEvents()
                self.pacman.update(dt)

        if self.flashBG:
            self.flashTimer += dt
            if self.flashTimer >= self.flashTime:
                self.flashTimer = 0
                if self.background == self.background_norm:
                    self.background = self.background_flash
                else:
                    self.background = self.background_norm

        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()

    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if not ghost.hunting_mode:
                ghost.checkHuntingMode(len(self.pellets.pelletList), self.pellets.max_quantity)
            if (self.pacman.x, self.pacman.y) == (ghost.x, ghost.y):
                if self.pacman.alive:
                    self.lives -= 1
                    self.lifesprites.removeImage()
                    self.pacman.die()
                    for hide_ghost in self.ghosts:
                        hide_ghost.visible = False
                    if self.lives <= 0:
                        self.textgroup.showText(GAMEOVERTXT)
                        self.pause.setPause(pauseTime=3, func=self.restartGame)
                    else:
                        self.pause.setPause(pauseTime=3, func=self.resetLevel)

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.alive:
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            self.textgroup.hideText()
                        else:
                            self.textgroup.showText(PAUSETXT)

    def checkPelletEvents(self):
        pellet = self.pacman.eat_pellet(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.updateScore(pellet.points)
            self.pellets.pelletList.remove(pellet)
            if self.pellets.isEmpty():
                self.flashBG = True
                self.pause.setPause(pauseTime=3, func=self.nextLevel())

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.pellets.render(self.screen)
        self.textgroup.render(self.screen)
        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))

        self.pacman.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
