import matplotlib.pyplot as plt
import matplotlib.animation as animation
from ai_fx import AIFX
from snake_process import Snake
from snake_radar import SnakeRadar
from snake_food import SnakeFood
from setup_input import SetupInput
from settings import Settings
from genetic_ai import GeneticAI
from utils import Utils
import json
from sys import stdout
from tqdm import tqdm

class App(Settings,Snake,SnakeRadar,SnakeFood,SetupInput,Utils,GeneticAI,AIFX):
    def __init__(self):
        super().__init__()
        self.mainrunFlag:bool = True
        self.saved = False
        self.pbar = None
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
    
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
            'NetworkLayers':self.NetworkLayers,
            'logs':self.logs
        }
        if not nogen:
            with open('Checkpoints/weight{}.json'.format(str(self.GenerationNR)),'w') as w:
                json.dump(weight_to_json,w)
        else:
            with open('weight.json','w') as w:
                json.dump(weight_to_json,w)
        
    def run(self):
        try:
            self.generatePopulations(True)
        except FileNotFoundError:
            self.generatePopulations()
        self.pbar = tqdm(total=len(self.SnakeBrain),leave=False,file=stdout)
        self.RandomPosition(3)
        while self.mainrunFlag:
            # Run Snake !!
            self.runSnake()
            self.steps -= 1
            if self.steps == 0:
                self.RESET_APP()
            if self.GenerationNR % 10 == 0 and not self.saved:
                self.checkpoints()
                self.saved = True
            

if __name__ == "__main__":
    App().run()