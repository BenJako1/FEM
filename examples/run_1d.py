from fem.d1.solver import HeatSolver1D
import numpy as np

sim = HeatSolver1D(k=0.2, A=0.1)
sim.build_mesh(L=1, N=20)
sim.assemble()

boundDict = {
    "nodes": [0, "0:19"],
    "type": ["temp", "convSurf"],
    "value": [100, np.array([1, 1, 20])]
}

sim.apply_boundary_conditions(boundDict)
T, Q = sim.solve()

from fem.d1.postprocess import plot_temperature
plot_temperature(sim.mesh.x, T)