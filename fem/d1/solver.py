import numpy as np
from fem.common.solver_base import SolverBase
from .assembly import assemble_1d
from .mesh import LineMesh1D
from .boundary import bound

class HeatSolver1D():
    def __init__(self, k, A):
        self.k = k
        self.A = A

    def build_mesh(self, L, N):
        self.mesh = LineMesh1D(L, N)
        self.N = N

    def assemble(self):
        self.K = assemble_1d(self.mesh, self.k, self.A)
    
    def apply_boundary_conditions(self, boundDict):
        self.T = np.zeros(self.N)
        self.Q = np.zeros(self.N)
        self.Convection = np.zeros(self.N)
        self.boundNodes = []

        bound(self, boundDict)

    def solve(self):
        K = np.copy(self.K)
        Q = np.copy(self.Q)

        # convection
        K += np.diag(self.Convection)

        # remove rows
        for count, bn in enumerate(self.boundNodes):
            K = np.delete(K, bn - count, axis=0)
            Q = np.delete(Q, bn - count, axis=0)

        # subtract known boundary temperatures
        for bn in self.boundNodes:
            Q -= K[:, bn] * self.T[bn]

        # remove columns
        for count, bn in enumerate(self.boundNodes):
            K = np.delete(K, bn - count, axis=1)

        T_unknown = np.linalg.solve(K, Q)

        Tsol = np.zeros(self.N)
        for i, fn in enumerate(self.freeNodes):
            Tsol[fn] = T_unknown[i]
        for bn in self.boundNodes:
            Tsol[bn] = self.T[bn]

        Qsol = self.K @ Tsol

        return Tsol, Qsol