import pygame as pg
from genetic_ai_fx import GENEAIFX
from snake_process import Snake
from snake_radar import SnakeRadar
from snake_food import SnakeFood
from setup_input import SetupInput
from settings import Settings
from genetic_ai import GeneticAI
from draw_neural import DrawNeural
from draw_stat import DrawStat
from utils import Utils
import sys
import json

class App(Settings,Snake,SnakeRadar,SnakeFood,SetupInput,Utils,GeneticAI,DrawNeural,GENEAIFX,DrawStat):
    def __init__(self):
        super().__init__()
        self.mainrunFlag:bool = True
        self.surface:object = None
        self.ct = 0
        
    def PygameInit(self):
        pg.init()
        self.surface = pg.display.set_mode(self.fullWinsize)
        self.surface.fill(self.BackgroundColor)
    
    def checkpoints(self,nogen = False):
        weight_to_json = {
            'Weight':[[y.tolist() for y in x.Brain] for x in self.SnakeBrain],
            'Bias':[[y.tolist() for y in x.Bias] for x in self.SnakeBrain],
            'Gen':self.GenerationNR,
            'Mft':self.HighFitness,
            'Msc':self.HighScore,
            'NN_Layers':self.NetworkLayers,
            'Actation_HDL':self.ActivationFunction_hdl,
            'Actation_OUT':self.ActivationFunction_output,
            'Selection':self.SelectionType,
            'CrossoverType':self.CrossoverType,
            'MutationType':self.MutationType,
            'MutationProp':self.mutation_prop,
            'NetworkLayers':self.NetworkLayers
        }
        if not nogen:
            with open('Checkpoints/weight{}.json'.format(str(self.GenerationNR)),'w') as w:
                json.dump(weight_to_json,w)
        else:
            with open('weight.json','w') as w:
                json.dump(weight_to_json,w)
    
    def checkExit(self):
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                self.checkpoints(True)
                self.mainrunFlag = False
                pg.quit()
                sys.exit()
                
    def run(self):
        self.PygameInit()
        if self.use_pretrained:
            self.generatePopulations(True)
        else:
            self.generatePopulations()
        self.pepare_node_xy(0.8)
        self.RandomPosition(3)
        self.init_stat()
        # clock = pg.time.Clock()
        while self.mainrunFlag:
            
            # clock.tick(self.SnakeSpeed)
            #check exit event
            self.checkExit()
            
            #draw snake's windows lines
            pg.draw.line( self.surface, ( 255,255,255 ), ( self.SnakeWinsize[0], 0 ), self.SnakeWinsize )
            pg.draw.line( self.surface, ( 255,255,255 ), self.SnakeWinsize, ( 0, self.SnakeWinsize[1] ) )
            
            # Run Snake !!
            if self.ct == self.SnakeSpeed * 50 or self.SnakeSpeed == 0:
                self.runSnake()
                self.steps -= 1
                if self.steps == 0:
                    self.RESET_APP()
                #global screen update
                pg.display.update()
                self.ct = 0
            self.ct += 1
            
            if self.GenerationNR % 10 == 0 and not self.saved:
                self.checkpoints()
                self.saved = True
            

if __name__ == "__main__":
    App().run()