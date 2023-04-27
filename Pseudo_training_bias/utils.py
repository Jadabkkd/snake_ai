import numpy as np
from tqdm import tqdm
from dot_dict import Dotdict
import matplotlib.pyplot as plt

class Utils(object):
    def __init__(self):
        super().__init__()
    
    def check_obj_direction(self,self_obj,compare_obj):
        key_ = None
        if self_obj[1] != compare_obj[1]:
            if self_obj[1] > compare_obj[1]:
                # if self_obj[0] > compare_obj[0]:
                #     key_ = ['U','L']
                # elif self_obj[0] < compare_obj[0]:
                #     key_ = ['U','R']
                # else:
                key_ = 'U'
            else:
                # if self_obj[0] > compare_obj[0]:
                #     key_ = ['D','L']
                # elif self_obj[0] < compare_obj[0]:
                #     key_ = ['D','R']
                # else:
                key_ = 'D'
        else:
            if self_obj[0] > compare_obj[0]:
                key_ = 'L'
            else:
                key_ = 'R'
        return self.one_hot_encode(key_)
       
    def one_hot_encode(self,inp):
        idx = self.classification.index(inp)
        outp_ = [0 if x != idx else 1 for x in range(len(self.classification))]
        return outp_
        
    def setupGrid(self):
        self.unUsedGrid.clear()
        gridSpace = lambda x : x * self.GridSize   
        for x in range( int( self.SnakeWinsize[0] / self.GridSize ) ):
            for y in range( int( self.SnakeWinsize[1] / self.GridSize ) ):
                self.unUsedGrid.append(
                    [gridSpace(x),gridSpace(y)]
                )
        
    def RESET_APP(self):
        self.movement : np.ndarray = np.array([0,0])
        self.eigth_marker: np.ndarray = None
        self.pos_to_edge_val: np.ndarray = None
        self.direction : str = ''
        self.SnakeBrain[self.PopulationNR-1].Score = self.RunningScore
        self.SnakeBrain[self.PopulationNR-1].Fitness = self.fitnessFX(self.RunningScore,self.steps)
        self.unUsedGrid.clear()
        self.SnakeBody.clear()
        self.occupied.clear()
        self.lastest_fit = self.SnakeBrain[self.PopulationNR-1].Fitness
        if self.SnakeBrain[self.PopulationNR-1].Fitness > self.HighFitness:
            self.HighFitness = self.SnakeBrain[self.PopulationNR-1].Fitness
        self.PopulationNR += 1
        self.pbar.update()
        if self.PopulationNR == len(self.SnakeBrain) + 1:
            parent_ = sorted(self.SnakeBrain, key = lambda i : i.Fitness)
            parent_.reverse()
            if self.GenerationNR == 1:
                self.ParentsForCRX = parent_
            else:
                self.ParentsForCRX = parent_[:self.Parents]
            self.pbar.update()
            self.pbar.close()
            print('Generation: {}  Best Fitness: {}  High Score: {}'.format(str(self.GenerationNR),str(self.ParentsForCRX[0].Fitness),str(self.ParentsForCRX[0].Score)))
            self.logs.append(Dotdict(
                Gnum = self.GenerationNR,
                Hscore = self.ParentsForCRX[0].Score
            ))
            self.init_roulette_wheel()
            self.Reproduce()
            self.pbar = tqdm(total=len(self.SnakeBrain))
            self.PopulationNR = 1
            self.GenerationNR += 1
            self.saved = False
        self.steps = self.maxsteps
        self.RandomPosition(3)
        self.RunningScore = 0