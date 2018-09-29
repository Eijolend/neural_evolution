from __future__ import print_function, division
import numpy as np



class World(object):
    def __init__(self, world_size, food_initial=(3, 2), food_growth=0.005, food_max=100):
        """
        """
        self.size = tuple(world_size)
        if isinstance(food_initial, (float, int)):
            self.state = food_initial * np.ones(self.size)
        elif isinstance(food_initial, tuple):
            food_initial, food_deviation = food_initial
            self.state = food_initial * np.ones(self.size) + np.random.uniform(low=-food_deviation, high=food_deviation, size=self.size)
        elif isinstance(food_initial, np.ndarray):

        else:
            raise ValueError("food_initial is of an unsupported type")
