from __future__ import print_function, division
import numpy as np
import pygame as pg
from itertools import product
from utils import hsv_color



class World(object):
    def __init__(self, world_size, food_initial=(3, 2), food_growth=0.005, food_max=100):
        """
        """
        self.size = tuple(world_size)
        self.food_max = 100
        self.food_growth = food_growth

        if isinstance(food_initial, (float, int)):
            self.state = food_initial * np.ones(self.size)
        elif isinstance(food_initial, tuple):
            food_initial, food_deviation = food_initial
            self.state = food_initial * np.ones(self.size) + np.random.uniform(low=-food_deviation, high=food_deviation, size=self.size)
            self.state[self.state < 0] = 0
            self.state[self.state > self.food_max] = self.food_max
        elif isinstance(food_initial, np.ndarray):
            self.state = food_initial
        else:
            raise ValueError("food_initial is of an unsupported type")



    def draw(self, screen, pos, dim):
        """
        """
        nx, ny = self.size
        dx = dim[0] / nx
        dy = dim[1] / ny
        for x, y in product(range(nx), range(ny)):
            pg.draw.rect(screen, hsv_color(0.33, self.state[x, y] / self.food_max, 1), (pos[0] + x * dx, pos[1] + y * dy, dx, dy))

    def loop(self):
        self.state = np.minimum(self.state + np.ones(self.size) * self.food_growth, np.ones(self.size) * self.food_max)
