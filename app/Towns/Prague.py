from .TownBase import TownBase


class Prague(TownBase):
    def __init__(self):
        self.name = 'Prague'
        self.x_growth = 0.008435
        self.y_growth = 0.013725
        self.x = 50.18
        self.y = 14.22