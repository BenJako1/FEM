import numpy as np
from .element import elemental_conductance
from .element import convection_stiffness, convection_load

def assemble_1d(mesh, k, A, Q_existing=None, verbose=False):
    N = mesh.N

    # Global stiffness matrix
    K = np.zeros((N, N))

    # Global force matrix
    F = np.zeros(N)

    # If explicit flux BCs exist, add them
    if Q_existing is not None:
        F += Q_existing

    for e, (n1, n2) in enumerate(mesh.elements):
        # Calculate element length
        Le = mesh.element_len[e]

        # Generate elemental conductivity matrix
        Ke = elemental_conductance(k, A, Le)
        K[n1:n2+1, n1:n2+1] += Ke
    
    if verbose:
        print(f'Conductivity matrix:\n{K}')
        print(f'Load vector: {F}')
    
    return K, F

def assemble_nonphys(mesh, F, convNodes=None, convElems=None):
    
    N = mesh.N

    Kn = np.zeros((N, N))

    # If there is not convection, create empty set
    if convNodes is None:
        convNodes = {}
    if convElems is None:
        convElems = {}

    for e, (n1, n2) in enumerate(mesh.elements):
        if e in convElems:
            h, Tinf, area = convElems[e]

            # convection stiffness/matrix
            Kc = convection_stiffness(h, area)
            Fc = convection_load(h, Tinf, area)

            # Add elemental conductivity and flux to global
            Kn[n1:n2+1, n1:n2+1] += Kc
            F[n1:n2+1] += Fc
    
    for n in mesh.nodes:
        if n in convNodes:
            h, Tinf, area = convNodes[n]

            Kn[n, n] += h * area
            F[n] += h * Tinf * area
    
    return Kn, F