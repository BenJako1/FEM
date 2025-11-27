import numpy as np

def element_B_matrix(x, y, A):
    return 1/(2*A)*np.array([
        [y[1]-y[2], y[2]-y[0], y[0]-y[1]],
        [x[2]-x[1], x[0]-x[2], x[1]-x[0]]])

def elemental_conductance(k, t, A, B):
    return k * t * A * (B.T @ B)

def convection_stiffness(h, t, Le):
    return h * t * Le / 6 * np.array([[2, 1],
                                      [1, 2]])

def convection_load(h, t, Tinf, Le):
    return h * t * Tinf * Le / 2 * np.array([1, 1])