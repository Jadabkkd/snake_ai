import numpy as np
from random import randint
from dot_dict import Dotdict
import json

class Snake(object):
    def __init__(self):
        super().__init__()
        self.SnakeBody : list[list] = []
        self.movementDict : Dotdict = Dotdict(
            L = np.array([-1,0]),
            R = np.array([1,0]),
            U = np.array([0,-1]),
            D = np.array([0,1]),
        )
        self.movement : np.ndarray = np.array([0,0])
        #food and space
        self.unUsedGrid:list[list] = []
        self.food_coor : list = []
        self.occupied = []
        
        #this for one hot encoded direction
        self.direction : str = ''
        
        #Score and fitness
        self.HighFitness = 0
        self.HighScore = 0
        self.RunningScore = 0
        self.lastest_fit = 0
        
            
    def RandomPosition(self,snk_len): #Random position for snake when start or reset
        ## Intialize grid box for snake's window
        self.setupGrid()
        ## 
        rnd = np.random.randint(low = 0,high = len(self.unUsedGrid) - 1,size = 1)[0]
        head_coor = np.array(self.unUsedGrid[rnd])
        init_direction = [['R','L'],['D','U']]
        x_or_y = randint(0,1)
        desc_asc = randint(0,1)
        self.direction = init_direction[x_or_y][desc_asc]
        self.movement = self.movementDict[self.direction]
        if desc_asc == 0:
            if head_coor[x_or_y] < self.GridSize * (snk_len): head_coor[x_or_y] = (self.GridSize * snk_len)
        else:
            if head_coor[x_or_y] > (self.SnakeWinsize[x_or_y] - (self.GridSize * snk_len)): head_coor[x_or_y] = self.SnakeWinsize[x_or_y] - (self.GridSize * (snk_len))
        for i in range(snk_len):
            if desc_asc == 0:
                body_init = head_coor.tolist()
                body_init[x_or_y] -= self.GridSize * i
            else:
                body_init = head_coor.tolist()
                body_init[x_or_y] += self.GridSize * i
            self.unUsedGrid.remove(body_init)
            x_y_tags = ["Y","X"]
            self.SnakeBody.append(
                Dotdict( tag = x_y_tags[x_or_y], coordinate = body_init )
            )
            self.occupied.append(body_init)
        self.prepare_and_feed(init=True)
        self.food_coor = None
        self.newFoodcoor()
    
    def runSnake(self):
        head_with_move = np.array(self.SnakeBody[0].coordinate) + self.movement
        #Give the tag for every box if X they have the same X if Y they have the same Y
        if self.direction == "L" or self.direction ==  "R":
            self.SnakeBody.insert(0,Dotdict( tag = "Y", coordinate = head_with_move.tolist() ))
        else:
            self.SnakeBody.insert(0,Dotdict( tag = "X", coordinate = head_with_move.tolist() ))
            
        snk_head_lis = self.SnakeBody[0].coordinate
        self.unUsedGrid.append(self.SnakeBody[-1].coordinate)
        if (snk_head_lis in self.unUsedGrid):
            
            if snk_head_lis not in self.occupied:
                self.occupied.append(snk_head_lis)
            
            if snk_head_lis[0] == self.food_coor[0] and snk_head_lis[1] == self.food_coor[1]:
                self.RunningScore += 1
                if self.RunningScore == 97:
                    self.HighScore = self.RunningScore
                    self.checkpoints(True)
                    self.RESET_APP()
                    self.steps = self.maxsteps
                else:
                    if self.RunningScore > self.HighScore:
                        self.HighScore = self.RunningScore
                    self.unUsedGrid.remove(snk_head_lis)
                    self.unUsedGrid.remove(self.SnakeBody[-1].coordinate)
                    self.newFoodcoor()
                    self.steps = self.maxsteps
            
            else:
                self.unUsedGrid.remove(snk_head_lis)
                self.SnakeBody.pop()
            self.prepare_and_feed()
        else:
            self.RESET_APP()
        
    
    def prepare_and_feed(self,init = False):
        if init:
            self.init_visions(np.array(self.SnakeBody[0].coordinate))
        else:
            self.modify_visions()
        self.groupBoxtoLine()
        self.checkVisions()
        # self.checkDirection()
        #turn input into numpy array before feed to network
        ai_out = self.FeedForward(np.array(self.AI_input))
        if np.array_equal((self.movementDict[ai_out] * self.GridSize) + self.movement\
            ,np.array([0,0])) == False:
            self.movement = self.movementDict[ai_out] * self.GridSize
            self.direction = ai_out