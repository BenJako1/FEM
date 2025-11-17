class SolverBase:
    def apply_boundary_conditions(self, *args, **kwargs):
        raise NotImplementedError

    def solve(self):
        raise NotImplementedError