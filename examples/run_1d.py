from fem.d1.solver import HeatSolver1D
from fem.d1.mesh import LineMesh1D
import numpy as np

sim = HeatSolver1D(k=0.2, A=200)
sim.mesh = LineMesh1D(L=120, N=20)

print(sim.mesh.nodes)

d1 = {
    "element": [f"0:{len(sim.mesh.elements)}"],
    "type": ["conv"],
    "value": [np.array([2e-4, 320, 30])]
}

d0 = {
    "node": [0, len(sim.mesh.x)-1],
    "type": ["temp", "conv"],
    "value": [330, np.array([2e-4, 30])]
}

sim.apply_boundary_conditions(d1, d0)
sim.assemble()
T, Q = sim.solve()

print(T)

from fem.d1.postprocess import plot_temperature
plot_temperature(sim.mesh.x, T)