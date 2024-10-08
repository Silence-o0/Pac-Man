class Pause:
    def __init__(self, paused=False):
        self.paused = paused
        self.timer = 0
        self.pauseTime = None
        self.func = None

    def update(self, dt):
        if self.pauseTime is not None:
            self.timer += dt
            if self.timer >= self.pauseTime:
                self.timer = 0
                self.paused = False
                self.pauseTime = None
                return self.func
        else:
            self.timer += dt
        return None

    def setPause(self, pauseTime=None, func=None, playerPaused = False):
        self.timer = 0
        self.func = func
        self.pauseTime = pauseTime
        self.flip()

    def flip(self):
        self.paused = not self.paused
