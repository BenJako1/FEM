from fem.common.solver_base import SolverBase

class HeatSolver3D(SolverBase):
    def __init__(self, k):
        self.k = k

    