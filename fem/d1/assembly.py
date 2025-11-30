import numpy as np
from .element import elemental_conductance
from .element import *
from fem.common.utils import edge_length

def assemble_1d(mesh, k, A):
    K = np.zeros((mesh.N, mesh.N))
    F = np.zeros(mesh.N)

    for element in mesh.elements:
        Le = edge_length(mesh.nodes[element])

        Ke = elemental_conductance(k, A, Le)
        K[np.ix_(element, element)] += Ke
    
    return K, F