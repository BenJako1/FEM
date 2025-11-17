import numpy as np

def assemble_1d(mesh, k, A):
    N = mesh.N
    K = np.zeros((N, N))

    for i, length in enumerate(mesh.element_len):
        Ke = k * A / length * np.array([[1, -1], [-1, 1]])
        n1, n2 = mesh.elements[i]

        K[n1, n1] += Ke[0, 0]
        K[n1, n2] += Ke[0, 1]
        K[n2, n1] += Ke[1, 0]
        K[n2, n2] += Ke[1, 1]

    return K