import numpy as np

def elemental_conductance(k, A, Le):
    return k * A / Le * np.array([[1, -1], [-1, 1]])

def convection_stiffness(h, Le):
    return h * Le / 6 * np.array([[2, 1],
                                  [1, 2]])

def convection_load(h, Tinf, Le):
    return h * Tinf * Le / 2 * np.array([1, 1])