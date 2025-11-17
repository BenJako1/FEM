import numpy as np

def element_conductance(k, A, length):
    c = k * A / length
    return c * np.array([[1, -1], [-1, 1]])