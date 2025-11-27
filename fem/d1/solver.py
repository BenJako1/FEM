import numpy as np
from fem.common.solver_base import SolverBase
from .assembly import assemble_1d, assemble_nonphys
from .mesh import LineMesh1D
from .boundary import bound

class HeatSolver1D(SolverBase):
    def __init__(self, k, A):
        self.k = k
        self.A = A

    def build_mesh(self, L, N):
        self.mesh = LineMesh1D(L, N)
    
    def apply_boundary_conditions(self, elementDict, nodeDict):
        bound(self, elementDict, nodeDict)
    
    def assemble(self):
        self.K, self.Q = assemble_1d(self.mesh,
                                     self.k,
                                     self.A,
                                     Q_existing=self.Q
                                    )
        Kconv, self.Q = assemble_nonphys(self.mesh,
                                         self.Q,
                                         convNodes=self.convNodes,
                                         convElems=self.convElems
                                        )
        self.Ksol = np.copy(self.K) + Kconv

    def solve(self):
        return SolverBase.solve(self)