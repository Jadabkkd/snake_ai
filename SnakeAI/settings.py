import pygame as pg
class Settings(object):
    def __init__(self):
        super().__init__()
        
        #Main app settings
        self.fullWinsize:tuple = (1200,700)
        self.BackgroundColor:str = (5, 0, 28)
    
        #snake settings
        self.SnakeWinsize:tuple = (400,400)
        self.GridSize:int = 40
        self.SnakeSpeed:int = 150 ### max speed is 0
        self.SnakeColor:tuple = (0, 116, 232)
        self.SnakeHeadColor = (247, 247, 247)
        self.SnakeFoodColor:tuple = (232, 85, 0)
        #max steps for Ai
        self.maxsteps = 100
        self.steps = self.maxsteps
        
        #AI settings
        self.classification = ["L","R","U","D"]
        self.Populations = 100
        self.Parents = 30
        self.NetworkLayers = [20,16,4] # output must be 4
        self.initPopType = 'Xavier'
        self.ActivationFunction_hdl = 'ReLu'
        self.ActivationFunction_output = 'Softmax'
        self.SelectionType = ['Roulette']
        self.CrossoverType = ['SBX','SPX']
        self.MutationType = ['Gaussian','Uniform']
        self.mutation_prop = 0.05
        self.mutation_edit = self.mutation_prop
        self.Keep_Parents = False
        self.FullPopulation = False
        
        #Status and Font
        pg.font.init()
        self.font_size = 24
        self.spacing = 32
        self.font = pg.font.SysFont('FC Subject [Non-commercial] Reg',self.font_size)
        self.saved = False
        self.stat_coor = {
            'max_fit':(10,self.SnakeWinsize[1] + self.spacing),
            'max_score':(10,self.SnakeWinsize[1] + self.spacing * 2),
            'gen_nr':(10,self.SnakeWinsize[1] + self.spacing * 3),
            'snk_nr':(10,self.SnakeWinsize[1] + self.spacing * 4),
            'cur_fit':(10,self.SnakeWinsize[1] + self.spacing * 5),
            'prev_score':(10,self.SnakeWinsize[1] + self.spacing * 6)
        }
        
        #Utils settings
        self.drawLine = False
        self.drawNeuralNet = True
        
        self.ifGridsizePossible()
        
    def ifGridsizePossible(self):
        if self.SnakeWinsize[0] % self.GridSize != 0 or self.SnakeWinsize[1] % self.GridSize != 0:
            raise ValueError("Grid size is not correct")