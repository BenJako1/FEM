import numpy as np
from .element import *

def assemble_2d(mesh, k, t):
    K = np.zeros((mesh.N, mesh.N))
    F = np.zeros(mesh.N)

    for e, nodes in enumerate(mesh.elements):
        x = mesh.x[nodes]
        y = mesh.y[nodes]
        B = element_B_matrix(x, y, mesh.A[e])
        Ke = elemental_conductance(k, t, mesh.A[e], B)

        K[np.ix_(nodes, nodes)] += Ke
    
    return K, F