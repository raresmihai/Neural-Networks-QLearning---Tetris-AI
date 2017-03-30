class Colors:
    # Define some colors
    def __init__(self):
        self.BLACK = (0, 0, 0)
        self.GREY = (200, 200, 200)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 51, 204)
        self.TURQUAISE = (51, 204, 204)
        self.ORANGE = (255, 153, 0)
        self.GREEN = (0, 204, 153)
        self.RED = (230, 0, 0)
        self.PURPLE = (204, 0, 153)
        self.PINK = (255, 0, 102)

    def getColors(self):
        return [self.BLUE, self.RED, self.ORANGE, self.GREEN, self.PURPLE, self.TURQUAISE, self.PINK]

    def getNonColors(self):
        return [self.BLACK, self.WHITE, self.GREY]
