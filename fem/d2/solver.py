import numpy as np
from fem.common.solver_base import SolverBase
from fem.common.boundary import Boundary
from .assembly import assemble_2d

class HeatSolver2D(SolverBase):
    def __init__(self, mesh, k, t):
        self.k = k
        self.t = t
        self.mesh = mesh
        self.boundary = Boundary(self)

    def assemble(self):
        self.K, self.Q = assemble_2d(self.mesh, self.k, self.t)
        self.T = np.zeros(self.mesh.N)

        self.K_sol = np.copy(self.K)
        self.Q_sol = np.copy(self.Q)

    def solve(self):
        return SolverBase.solve(self)