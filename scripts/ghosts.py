from scripts.directions_algorithms import DirectionMethods
from scripts.entity import Entity
from scripts.sprites import GhostSprites


class Ghost(Entity):
    def __init__(self, home, maze, pacman=None, name=None, time=0):
        super().__init__(home[0], home[1], maze)
        self.name = name
        self.pacman_following = False
        self.pacman = pacman
        self.speed = 50
        self.start_time = time
        self.hunting_mode = False
        self.sprites = GhostSprites(self)

    def ghost_move(self):
        if self.hunting_mode:
            self.current_direction = DirectionMethods.bfs_to_pacman(self, self.grid,
                                                                    (self.pacman.x, self.pacman.y))
        else:
            self.current_direction = DirectionMethods.random_move(self, self.grid)
        self.set_move()

    def update(self, dt):
        if self.current_direction == "STOP":
            self.ghost_move()

        if (self.x_pixels, self.y_pixels) != self.goal_point:
            diff = self.speed * dt
            if abs(self.goal_point[0] - self.x_pixels) < diff + 0.5 and abs(self.goal_point[1] - self.y_pixels) < diff + 0.5:
                self.x_pixels = self.goal_point[0]
                self.y_pixels = self.goal_point[1]
                self.x = self.goal_cell[0]
                self.y = self.goal_cell[1]
                self.ghost_move()
            else:
                x_displace = self.goal_cell[0] - self.x
                y_displace = self.goal_cell[1] - self.y
                self.x_pixels = self.x_pixels + (self.speed * dt) * x_displace
                self.y_pixels = self.y_pixels + (self.speed * dt) * y_displace

        self.sprites.update(dt)

    def checkHuntingMode(self, cur_pellets_quantity, max_pellets_quantity):
        if cur_pellets_quantity < 0.75 * max_pellets_quantity:
            self.hunting_mode = True
