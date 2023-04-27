import numpy as np
import pygame as pg
from dot_dict import Dotdict

class Utils(object):
    def __init__(self):
        super().__init__()
    
    def check_obj_direction(self,self_obj,compare_obj):
        key_ = None
        if self_obj[1] != compare_obj[1]:
            if self_obj[1] > compare_obj[1]:
                key_ = 'U'
            else:
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
        if not self.unUsedGrid:
            gridSpace = lambda x : x * self.GridSize   
            for x in range( int( self.SnakeWinsize[0] / self.GridSize ) ):
                for y in range( int( self.SnakeWinsize[1] / self.GridSize ) ):
                    self.unUsedGrid.append(
                        [gridSpace(x),gridSpace(y)]
                    )
                    self.unUsedGrid_temp.append(
                        [gridSpace(x),gridSpace(y)]
                    )
        else:
            self.unUsedGrid.clear()
            self.unUsedGrid = self.unUsedGrid_temp.copy()
    def calc_dist(self,p1,p2):
        dist = np.sqrt(np.sum(np.abs(p2-p1)**2))
        return round(abs(dist),4)
    
    def drawVisionLine(self,start,end,color_stat = 'none'):
        color_list = {
            'none':(255,255,255),
            'food':(81, 224, 40),
            'body':(235, 52, 113),
            'remove':self.BackgroundColor
        }
        pg.draw.line(self.surface,color_list[color_stat],start,end)
        
    
    def drawBox(self,xy,_color):
        pg.draw.rect(
            self.surface,
            _color,
            (xy,(self.GridSize-1,self.GridSize-1)),
            border_radius=1
        )
        
    def RESET_APP(self):
        pg.draw.rect(self.surface,self.BackgroundColor,([0,0],self.SnakeWinsize))
        self.movement : np.ndarray = np.array([0,0])
        self.eigth_marker: np.ndarray = None
        self.pos_to_edge_coor: np.ndarray = None
        self.direction : str = ''
        self.SnakeBrain[self.PopulationNR-1].Score = self.RunningScore
        self.SnakeBrain[self.PopulationNR-1].Fitness = self.fitnessFX(self.RunningScore,self.steps)
        self.SnakeBody.clear()
        self.occupied.clear()
        self.lastest_fit = self.SnakeBrain[self.PopulationNR-1].Fitness
        self.update_stat('Prev Fitness: ',self.lastest_fit,'cur_fit')
        self.update_stat('Prev Score: ',self.RunningScore,'prev_score')
        if self.SnakeBrain[self.PopulationNR-1].Fitness > self.HighFitness:
            self.HighFitness = self.SnakeBrain[self.PopulationNR-1].Fitness
            self.update_stat('Best fitness: ',self.HighFitness,'max_fit')
        self.PopulationNR += 1
        if self.PopulationNR == len(self.SnakeBrain) + 1:
            parent_ = sorted(self.SnakeBrain, key = lambda i : i.Fitness)
            parent_.reverse()
            if self.GenerationNR == 1:
                self.ParentsForCRX = parent_
            else:
                self.ParentsForCRX = parent_[:self.Parents]
            print('Generation: {}  Best Fitness: {}  High Score: {} AT Nr.: {}'.format(str(self.GenerationNR),str(self.ParentsForCRX[0].Fitness),str(self.ParentsForCRX[0].Score),str(self.ParentsForCRX[0].NR)))
            self.logs.append(Dotdict(
                Gnum = self.GenerationNR,
                Hscore = self.ParentsForCRX[0].Score
            ))
            self.init_roulette_wheel()
            self.Reproduce()
            self.PopulationNR = 1
            self.GenerationNR += 1
            self.update_stat('Generation: ',self.GenerationNR,'gen_nr')
            self.saved = False
        self.steps = self.maxsteps
        self.RandomPosition(3)
        self.update_stat('Snake Number: ',self.PopulationNR,'snk_nr')
        self.RunningScore = 0