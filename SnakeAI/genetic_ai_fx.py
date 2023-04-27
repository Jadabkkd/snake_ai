import numpy as np
from random import choice, randint, shuffle, uniform
from math import sqrt

class GENEAIFX(object):
    def __init__(self):
        super().__init__()

    def roulette_wheel_selection(self):
        roulette_board = self.roulette_wheel
        parents_idx1 = []
        parents_idx2 = []
        temp_parent_idx1 = None
        temp_parent_idx2 = None
        
        rand1 = uniform(roulette_board[-1],roulette_board[0])
        for ir1 in range(len(roulette_board)-1):
            if roulette_board[ir1+1] <= rand1 <= roulette_board[ir1]:
                temp_parent_idx1 = ir1
        for idx,i2 in enumerate(roulette_board):
            if roulette_board[temp_parent_idx1] == i2:
                parents_idx1.append(idx)
                
        rand2 = uniform(roulette_board[-1],roulette_board[0])
        for ir2 in range(len(roulette_board)-1):
            if roulette_board[ir2+1] <= rand2 <= roulette_board[ir2]:
                temp_parent_idx2 = ir2
        for idx2,i22 in enumerate(roulette_board):
            if roulette_board[temp_parent_idx2] == i22:
                parents_idx2.append(idx2)
                
        parents_idx1 = choice(parents_idx1)
        parents_idx2 = choice(parents_idx2)
        if parents_idx1 == parents_idx2:
            if parents_idx1 == len(roulette_board)-1:
                parents_idx2 -= 1
            else:
                parents_idx2 += 1
        return parents_idx1, parents_idx2

    def tournament_selection(self):
        fighter = []
        parents_arr = [x for x in range(len(self.ParentsForCRX) - 1)]
        for i in range(10):
            p_idx = parents_arr[randint(0,len(parents_arr)-1)]
            fighter.append(p_idx)
            parents_arr.remove(p_idx)

        shuffle(fighter)
        winner1 = None
        winner2 = None
        fighter_group1 = fighter[:int(len(fighter)/2)]
        for f in fighter_group1:
            if winner1 == None:
                winner1 = f
            elif self.ParentsForCRX[f-1].Fitness < self.ParentsForCRX[f].Fitness:
                winner1 = f
        fighter_group2 = fighter[int(len(fighter)/2):]
        for f in fighter_group2:
            if winner2 == None:
                winner2 = f
            elif self.ParentsForCRX[f-1].Fitness < self.ParentsForCRX[f].Fitness:
                winner2 = f
        return winner1,winner2
    
    def SBX(self,parent1W, parent2W, parent1B, parent2B):
        child1W = []
        child2W = []
        child1B = []
        child2B = []
        eta = 100
        for idx,(W,B) in enumerate(zip(parent1W,parent1B)):
            #weight session
            randW = np.random.random(W.shape).astype(np.float64)
            gammaW = np.empty(W.shape)
            gammaW[randW <= 0.5] = (2 * randW[randW <= 0.5]) ** (1.0 / (eta + 1))
            gammaW[randW > 0.5] = (1.0 / (2.0 * (1.0 - randW[randW > 0.5]))) ** (1.0 / (eta + 1))
            chromosome1W = 0.5 * ((1 + gammaW)*parent1W[idx] + (1 - gammaW)*parent2W[idx])
            chromosome2W = 0.5 * ((1 - gammaW)*parent1W[idx] + (1 + gammaW)*parent2W[idx])
            child1W.append(chromosome1W.astype(np.float64))
            child2W.append(chromosome2W.astype(np.float64))
            #bias session
            randB = np.random.random(B.shape).astype(np.float64)
            gammaB = np.empty(B.shape)
            gammaB[randB <= 0.5] = (2 * randB[randB <= 0.5]) ** (1.0 / (eta + 1))
            gammaB[randB > 0.5] = (1.0 / (2.0 * (1.0 - randB[randB > 0.5]))) ** (1.0 / (eta + 1))
            chromosome1B = 0.5 * ((1 + gammaB)*parent1B[idx] + (1 - gammaB)*parent2B[idx])
            chromosome2B = 0.5 * ((1 - gammaB)*parent1B[idx] + (1 + gammaB)*parent2B[idx])
            child1B.append(chromosome1B.astype(np.float64))
            child2B.append(chromosome2B.astype(np.float64))
        return child1W,child2W,child1B,child2B
        

    def SPX(self,parent1W, parent2W, parent1B, parent2B):
        child1W = []
        child2W = []
        child1B = []
        child2B = []
        for idx, W in enumerate(parent1W):
            #weight session
            crx_point = randint(0,W.shape[0] - 1)
            off_spring1W = np.concatenate((parent1W[idx][ crx_point: ],parent2W[idx][ :crx_point ]))
            off_spring2W = np.concatenate((parent2W[idx][ crx_point: ],parent1W[idx][ :crx_point ]))
            child1W.append(off_spring1W)
            child2W.append(off_spring2W)
            #bias session
            off_spring1B = np.concatenate((parent1B[idx][ crx_point: ],parent2B[idx][ :crx_point ]))
            off_spring2B = np.concatenate((parent2B[idx][ crx_point: ],parent1B[idx][ :crx_point ]))
            child1B.append(off_spring1B)
            child2B.append(off_spring2B)
        return child1W,child2W,child1B,child2B
    
    def GaussianMutation(self,child1W,child2W,child1B,child2B):
        child1_MuW = []
        child2_MuW = []
        child1_MuB = []
        child2_MuB = []
        for c1W,c2W,c1B,c2B in zip(child1W,child2W,child1B,child2B):
            #wight session
            cromosome_propsW = np.random.random(c1W.shape) < self.mutation_prop
            gaus_valW = np.random.normal(size = c1W.shape)
            c1W[cromosome_propsW] += gaus_valW[cromosome_propsW]
            c2W[cromosome_propsW] += gaus_valW[cromosome_propsW]
            child1_MuW.append(c1W)
            child2_MuW.append(c2W)
            #bias session
            cromosome_propsB = np.random.random(c1B.shape) < self.mutation_prop
            gaus_valB = np.random.normal(size = c1B.shape)
            c1B[cromosome_propsB] += gaus_valB[cromosome_propsB]
            c2B[cromosome_propsB] += gaus_valB[cromosome_propsB]
            child1_MuB.append(c1B)
            child2_MuB.append(c2B)
        return child1_MuW,child2_MuW,child1_MuB,child2_MuB
    
    def Uniform_Mutation(self,child1W,child2W,child1B,child2B):
        child1_MuW = []
        child2_MuW = []
        child1_MuB = []
        child2_MuB = []
        for c1W,c2W,c1B,c2B in zip(child1W,child2W,child1B,child2B):
            #wight session
            cromosome_propsW = np.random.random(c1W.shape) < self.mutation_prop
            uni_valW = np.random.uniform(low=-1,high=1,size = c1W.shape)
            c1W[cromosome_propsW] += uni_valW[cromosome_propsW]
            c2W[cromosome_propsW] += uni_valW[cromosome_propsW]
            child1_MuW.append(c1W)
            child2_MuW.append(c2W)
            #bias session
            cromosome_propsB = np.random.random(c1B.shape) < self.mutation_prop
            uni_valB = np.random.uniform(low=-1,high=1,size = c1B.shape)
            c1B[cromosome_propsB] += uni_valB[cromosome_propsB]
            c2B[cromosome_propsB] += uni_valB[cromosome_propsB]
            child1_MuB.append(c1B)
            child2_MuB.append(c2B)
        return child1_MuW,child2_MuW,child1_MuB,child2_MuB
    
    def Xavier_Bias_initialization(self,x): #for bias
        Umin,Umax = -(1/sqrt(x)),(1/sqrt(x))
        rand_weight = np.random.rand(x)
        weight = Umin + rand_weight * (Umax - Umin)
        return weight

    def Xavier_Normal_initialization(self,x,y): #for non-linear activation function
        Umin,Umax = -(1/sqrt(x + y)),(1/sqrt(x + y))
        rand_weight = np.random.rand(x,y)
        weight = Umin + rand_weight * (Umax - Umin)
        return weight

    def Xavier_ReLu_initialization(self,x,y): #for ReLu
        std = sqrt(2/x)
        rand_weight = np.random.randn(x,y)
        weight = rand_weight * std
        return weight
    
    def Xavier_Main(self,x,y = None):
        if not y:
            return self.Xavier_Bias_initialization(x)
        elif y == 4:
            if self.ActivationFunction_output == 'ReLu':
                return self.Xavier_ReLu_initialization(x,y)
            else:
                return self.Xavier_Normal_initialization(x,y)
        else:
            if self.ActivationFunction_hdl == 'ReLu':
                return self.Xavier_ReLu_initialization(x,y)
            else:
                return self.Xavier_Normal_initialization(x,y)