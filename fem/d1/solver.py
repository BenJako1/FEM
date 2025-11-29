import numpy as np
from fem.common.solver_base import SolverBase
from fem.common.boundary import Boundary
from .assembly import assemble_1d

class HeatSolver1D(SolverBase):
    def __init__(self, mesh, k, A):
        self.k = k
        self.A = A
        self.mesh = mesh
        self.boundary = Boundary(self)
    
    def assemble(self):
        self.K, self.Q = assemble_1d(self.mesh, self.k, self.A)
        self.T = np.zeros(self.mesh.N)
        
        self.K_sol = np.copy(self.K)
        self.Q_sol = np.copy(self.Q)

    def solve(self):
        return SolverBase.solve(self)