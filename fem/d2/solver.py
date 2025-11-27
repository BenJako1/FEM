import numpy as np
from fem.common.solver_base import SolverBase
from .assembly import assemble_2d, assemble_nonphys
from .mesh import TriMesh2D
from .boundary import bound

class HeatSolver2D():
    def __init__(self, k, t):
        self.k = k
        self.t = t

    def build_mesh(self, L, H, nx, ny):
        self.mesh = TriMesh2D(L, H, nx, ny)

    def apply_boundary_conditions(self, elementDict, edgeDict, nodeDict):
        bound(self, elementDict, edgeDict, nodeDict)

    def assemble(self):
        self.K = assemble_2d(self.mesh, self.k, self.t)
        Kconv, self.Q = assemble_nonphys(self.mesh,
                                         self.Q,
                                         self.t,
                                         convBC=self.convBC)
        self.Ksol = np.copy(self.K) + Kconv

    def solve(self):
        return SolverBase.solve(self)