import numpy as np
import random

class SnakeFood(object):
    def __init__(self):
        super().__init__()
    
    def newFoodcoor(self):
        seed = np.random.randint(-100000,100000)
        rand = random.Random(seed)
        food_coor = rand.choice(self.unUsedGrid)
        self.food_coor = food_coor
        xf_min = self.food_coor[0]
        yf_min = self.food_coor[1]
        xf_max = self.food_coor[0] + self.GridSize
        yf_max = self.food_coor[1] + self.GridSize
        lf1 = [ [ xf_min, yf_min ],[ xf_max, yf_min ] ]
        lf2 = [ [ xf_min, yf_max ] , [ xf_max, yf_max ] ]
        lf3 = [ [ xf_min, yf_min ] , [ xf_min, yf_max ] ]
        lf4 = [ [ xf_max, yf_min ] , [ xf_max, yf_max ] ]
        lf5 = [ [ ((xf_max - xf_min)/2) + xf_min, yf_min ],[ ((xf_max - xf_min)/2)+xf_min, yf_max ] ]
        self.foodOutlines = [lf1,lf2,lf3,lf4,lf5]
        