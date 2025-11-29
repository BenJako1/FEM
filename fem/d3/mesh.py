import numpy as np

class TetMesh3D:
    def __init__(self, L, W, H, nx, ny, nz):
        self.N = nx*ny*nz

        self.x = np.zeros(self.N)
        self.y = np.zeros(self.N)
        self.z = np.zeros(self.N)
        for k in range(nz):
            for j in range(ny):
                for i in range(nx):
                    idx = k*(nx*ny) + j*nx + i
                    x = L * i / (nx - 1)
                    y = H * j / (ny - 1)
                    z = W * k / (nz - 1)
                    self.x[idx] = x
                    self.y[idx] = y
                    self.z[idx] = z

        # Generate elements from quads
        self.elements = np.zeros(((nx - 1)*(ny - 1)*(nz - 1)*5, 4), dtype=int)

        count = 0
        for k in range(nz - 1):
            for j in range(ny - 1):
                for i in range(nx - 1):

                    # local quad nodes
                    A = k*(nx*ny) + j*nx + i
                    B = A + 1
                    D = A + nx
                    C = D + 1     # (j+1)*nx + (i+1)
                    E = A + (nx*ny)
                    F = E + 1
                    H = E + nx
                    G = H + 1

                    self.elements[count, :] = [A, B, D, E]
                    count += 1
                    self.elements[count, :] = [B, E, F, G]
                    count += 1
                    self.elements[count, :] = [B, C, D, G]
                    count += 1
                    self.elements[count, :] = [D, E, G, H]
                    count += 1
                    self.elements[count, :] = [B, D, E, G]
                    count += 1
        
        # Extract node coordinates for each tet
        x = self.x[self.elements]
        y = self.y[self.elements]
        z = self.z[self.elements]

        # Build edge vectors v2-v1, v3-v1, v4-v1 for all elements
        v21 = np.column_stack((x[:,1] - x[:,0],
                            y[:,1] - y[:,0],
                            z[:,1] - z[:,0]))

        v31 = np.column_stack((x[:,2] - x[:,0],
                            y[:,2] - y[:,0],
                            z[:,2] - z[:,0]))

        v41 = np.column_stack((x[:,3] - x[:,0],
                            y[:,3] - y[:,0],
                            z[:,3] - z[:,0]))

        # Stack into a batch of 3×3 matrices: shape (Ne, 3, 3)
        M = np.stack((v21, v31, v41), axis=1)
        self.V = np.abs(np.linalg.det(M)) / 6.0