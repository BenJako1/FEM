import numpy as np

class TetMesh3D:
    def __init__(self, L, W, H, nx, ny, nz):
        self.N = nx*ny*nz
        # Generate nodes
        self.nodes = np.zeros((self.N, 2))
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
                    self.nodes[idx] = [x, y, z]
                    self.x[idx] = x
                    self.y[idx] = y
                    self.z[idx] = z

        # Generate elements from quads
        self.elements = np.zeros(((nx - 1)*(ny - 1)*(nz - 1)*4, 4), dtype=int)

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
        
        tets = self.nodes[self.elements]
        x1, y1, z1 = tets[:,0,0], tets[:,0,1]
        x2, y2, z2 = tets[:,1,0], tets[:,1,1]
        x3, y3, z3 = tets[:,2,0], tets[:,2,1]

        self.V = 0.5 * np.abs(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2))