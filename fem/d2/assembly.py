import numpy as np
from .element import element_B_matrix, elemental_conductance, convection_stiffness, convection_load

def assemble_2d(mesh, k, t):
    N = mesh.N
    K = np.zeros((N, N))
    for e, nodes in enumerate(mesh.elements):
        x = mesh.x[nodes]
        y = mesh.y[nodes]
        B = element_B_matrix(x, y, mesh.A[e])
        Ke = elemental_conductance(k, t, mesh.A[e], B)

        K[np.ix_(nodes, nodes)] += Ke

        """K[mesh.elements[e][0],mesh.elements[e][0]] += Ke[0,0]
        K[mesh.elements[e][1],mesh.elements[e][0]] += Ke[1,0]
        K[mesh.elements[e][2],mesh.elements[e][0]] += Ke[2,0]
        K[mesh.elements[e][0],mesh.elements[e][1]] += Ke[0,1]
        K[mesh.elements[e][1],mesh.elements[e][1]] += Ke[1,1]
        K[mesh.elements[e][2],mesh.elements[e][1]] += Ke[2,1]
        K[mesh.elements[e][0],mesh.elements[e][2]] += Ke[0,2]
        K[mesh.elements[e][1],mesh.elements[e][2]] += Ke[1,2]
        K[mesh.elements[e][2],mesh.elements[e][2]] += Ke[2,2]"""
    
    return K

def assemble_nonphys(mesh, F, t, convBC=None):
    
    N = mesh.N

    Kn = np.zeros((N, N))

    # If there is not convection, create empty set
    if convBC is None:
        convBC = {}

    for nodes, h, T_inf, length in convBC:
        Kc = convection_stiffness(h, t, length)
        Fc = convection_load(h, t, T_inf, length)
        
        Kn[np.ix_(nodes, nodes)] += Kc
        F[nodes] += Fc
    
    return Kn, F