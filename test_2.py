import numpy as np
from utils.calc_d_prime import calc_d_prime

# perfect observer example (finite with loglinear correction)
print(calc_d_prime(50, 0, 0, 50))  # ~ large positive (finite)
# array signature example
stim = np.array([0,0,0,1,1,1])
resp = np.array([0,0,1,1,1,0])
print(calc_d_prime(stim, resp))    # finite float
