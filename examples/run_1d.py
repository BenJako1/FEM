from fem.d1.solver import HeatSolver1D
import numpy as np

sim = HeatSolver1D(k=0.2, A=200)
sim.build_mesh(L=120, N=20)

elementDict = {
    "element": ["0:19"],
    "type": ["convSurf"],
    "value": [np.array([2e-4, 320, 30])]
}

nodeDict = {
    "node": [0, 19],
    "type": ["temp", "convFace"],
    "value": [330, np.array([2e-4, 30])]
}

sim.apply_boundary_conditions(elementDict, nodeDict)
sim.assemble()
T, Q = sim.solve()

print(T)
print(Q)

from fem.d1.postprocess import plot_temperature
plot_temperature(sim.mesh.x, T)
plot_temperature(sim.mesh.x, Q)