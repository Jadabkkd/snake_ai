import numpy as np
from dot_dict import Dotdict
from random import choice
import json

class GeneticAI(object):
    def __init__(self):
        super().__init__()
        self.SnakeBrain:list[dict] = []
        self.ParentsForCRX:list[dict] = []
        self.logs:list[dict] = []
        self.GenerationNR = 1
        self.PopulationNR = 1
        
        self.activationFX:dict = {
            'ReLu':lambda x : np.maximum(0,x),
            'Sigmoid': lambda x : 1 / (1+np.exp(-x).astype(np.float64)),
            'Tanh':lambda x : np.tanh(x).astype(np.float64),
            'LeakyReLu':lambda x: np.where(x > 0, x, x * 0.01).astype(np.float64),
            'Softmax':lambda x : np.exp(x) / np.exp(np.sum(x).astype(np.float64)),
            'Softsign':lambda x : x / (1 + np.abs(x)),
            'Softplus':lambda x : np.log(1+np.exp(x)),
            'Linear':lambda x : x
        }
        
        self.SelectionFX:dict = {
            'Roulette': self.roulette_wheel_selection,
            'Tour': self.tournament_selection
        }
        
        self.CrossOverFX:dict = {
            'SBX': lambda p1W,p2W,p1B,p2B : self.SBX(p1W,p2W,p1B,p2B),
            'SPX': lambda p1W,p2W,p1B,p2B : self.SPX(p1W,p2W,p1B,p2B)
        }
        
        self.MutationFX:dict = {
            'Gaussian': lambda c1W,c2W,c1B,c2B : self.GaussianMutation(c1W,c2W,c1B,c2B),
            'Uniform': lambda c1W,c2W,c1B,c2B : self.Uniform_Mutation(c1W,c2W,c1B,c2B)
        }
        
        self.initPopFX:dict = {
            'Gaussian': lambda x, y = None : np.random.normal(size=(x,y)) if y else np.random.normal(size=(x,)),
            'Uniform': lambda x, y = None : np.random.uniform(low = -2, high = 2, size=(x,y)) if y else np.random.uniform(low = -1, high = 1, size=(x,)),
            'Xavier': lambda x, y = None : self.Xavier_Main(x,y)
        }
        
        # for visualize NN
        self.w_list:list[np.ndarray] = []
        # for roulette wheel
        self.roulette_wheel:list = []
    
    def init_roulette_wheel(self):
        sum_fit = sum([x.Fitness for x in self.ParentsForCRX])
        self.roulette_wheel = [x.Fitness / sum_fit for x in self.ParentsForCRX]
        
    def generatePopulations(self,jsonf = False):
        if jsonf:
            f = open('weight.json',)
            weight = json.load(f)
            for i,(_allw,_allb) in enumerate(zip(weight['Weight'],weight['Bias'])):
                self.SnakeBrain.append(
                    Dotdict(Brain = [np.array(x) for x in _allw], Bias = [np.array(x) for x in _allb], Score = 0, Fitness = 0,NR = i)
                )
            # self.SnakeBrain.reverse()
            self.GenerationNR = weight['Gen']
            self.HighFitness = weight['Mft']
            self.HighScore = weight['Msc']
            self.ActivationFunction_hdl = weight['Actation_HDL']
            self.ActivationFunction_output = weight['Actation_OUT']
            self.SelectionType = weight['Selection']
            self.CrossoverType = weight['CrossoverType']
            self.MutationType = weight['MutationType']
            self.mutation_prop = weight['MutationProp']
            self.NetworkLayers = weight['NetworkLayers']
            self.logs = weight['logs']
        else:
            popnum = self.Populations
            if self.FullPopulation:
                popnum = self.Populations + self.Parents
            self.NetworkLayers.insert(0,24)
            for _ in range(popnum):
                network_ = []
                bias_ = []
                for i,w in enumerate(self.NetworkLayers):
                    if i == 0:
                        pass
                    else:
                        hdl = self.initPopFX[self.initPopType](self.NetworkLayers[i-1],w)
                        b = self.initPopFX[self.initPopType](w)
                        network_.append(hdl.astype(np.float64))
                        bias_.append(b.astype(np.float64))
                self.SnakeBrain.append(
                    Dotdict(Brain = network_, Bias = bias_ , Score = 0, Fitness = 0, NR = _)
                )
            
    def FeedForward(self, inputs_):
        w: np.ndarray
        w_list = []
        for i,(n,b) in enumerate(zip(self.SnakeBrain[self.PopulationNR-1].Brain,self.SnakeBrain[self.PopulationNR-1].Bias)):
            if i == 0:
                w_list.append(inputs_)
                w = inputs_.dot(n).astype(np.float64)
                w += b
                w = self.activationFX[self.ActivationFunction_hdl](w)
                w_list.append(w)
            elif i < len(self.SnakeBrain[self.PopulationNR-1].Brain) - 1:
                w = w.dot(n).astype(np.float64)
                w += b
                w = self.activationFX[self.ActivationFunction_hdl](w)
                w_list.append(w)
            else:
                w = w.dot(n).astype(np.float64)
                w += b
        _out = self.activationFX[self.ActivationFunction_output](w)
        w_list.append(self.one_hot_encode(self.classification[np.argmax(_out)]))
        self.w_list = w_list
        _out = self.classification[np.argmax(_out)]
        return _out
    
    def Reproduce(self):
        self.SnakeBrain.clear()
        if self.HighScore != 0:
            self.mutation_prop = ((97 - self.HighScore) / 97) * self.mutation_edit
        print(self.mutation_prop)
        for _ in range(int(self.Populations/2)):
            p1_idx,p2_idx = self.SelectionFX[choice(self.SelectionType)]()
            parent1W, parent1B = self.ParentsForCRX[p1_idx].Brain, self.ParentsForCRX[p1_idx].Bias
            parent2W,parent2B = self.ParentsForCRX[p2_idx].Brain, self.ParentsForCRX[p2_idx].Bias
            child1W,child2W,child1B,child2B = self.CrossOverFX[choice(self.CrossoverType)](parent1W,parent2W,parent1B,parent2B)
            child1W,child2W,child1B,child2B = self.MutationFX[choice(self.MutationType)](child1W,child2W,child1B,child2B)
            self.SnakeBrain.extend([
                Dotdict(Brain = child1W, Bias = child1B, Score = 0, Fitness = 0, Rank = p1_idx + p2_idx, NR = _ * 2),
                Dotdict(Brain = child2W,  Bias = child2B, Score = 0, Fitness = 0, Rank = p1_idx + p2_idx, NR = (_ * 2) + 1)
            ])
        self.SnakeBrain = sorted(self.SnakeBrain, key = lambda i : i.Rank)
        if self.Keep_Parents:
            for p in self.ParentsForCRX:
                self.SnakeBrain.append(
                    Dotdict(Brain = p.Brain , Score = 0, Fitness = 0)
                )
        self.ParentsForCRX.clear()
            
    
    def fitnessFX(self,score,steps):
        fit_val = ((score * 200) + (steps + len(self.occupied)))
        return fit_val