TILEWIDTH = 20
TILEHEIGHT = 20
PARTTILEWIDTH = TILEWIDTH - (TILEWIDTH/2)
PARTTILEHEIGHT = TILEHEIGHT - (TILEHEIGHT/2)
NROWS = 24
NCOLS = 24
LEFT_INDENT = 50
TOP_INDENT = 50
SCREENWIDTH = NCOLS * TILEWIDTH + LEFT_INDENT * 2
SCREENHEIGHT = NROWS * TILEHEIGHT + TOP_INDENT * 2
SCREENSIZE = (SCREENWIDTH, SCREENHEIGHT)
BLACK = (0, 0, 0)

YELLOW = (255, 255, 0)

BASETILEWIDTH = 16
BASETILEHEIGHT = 16

WALL_COLOR = (22, 46, 70)
PATH_COLOR = (56, 158, 169)
HOUSE_COLOR = (129, 35, 126)

STOP = 0
UP = 1
DOWN = -1
LEFT = 2
RIGHT = -2
PORTAL = 3

PACMAN = 0
PELLET = 1
POWERPELLET = 2
GHOST = 3

WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 100, 150)
TEAL = (100, 255, 255)
ORANGE = (230, 190, 40)
GREEN = (0, 255, 0)

SCATTER = 0
CHASE = 1
FREIGHT = 2
SPAWN = 3

BLINKY = 4
PINKY = 5
INKY = 6
CLYDE = 7
FRUIT = 8

SCORETXT = 0
LEVELTXT = 1
READYTXT = 2
PAUSETXT = 3
GAMEOVERTXT = 4

DEATH = 5