from setup_input import SetupInput
import numpy as np
x = np.array([60,20])
y = np.array([100,50])
a = SetupInput().calc_dist(y,x)
print(a)