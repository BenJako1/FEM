from fem.d1.solver import HeatSolver1D
from fem.d2.mesh import TriMesh2D
from fem.d1.mesh import LineMesh1D
import numpy as np

mesh = LineMesh1D(120, 4)

sim = HeatSolver1D(k=0.2, A=200, mesh=mesh)
sim.assemble()

h, T_inf = 2e-4, 30

sim.boundary.apply_conv1d(mesh.elements, h, 320, T_inf)
sim.boundary.apply_conv0d(3, h, sim.A, T_inf)
sim.boundary.apply_temp0d(0, 330)

T, Q = sim.solve()

print(T)

from fem.d1.postprocess import plot_temperature

plot_temperature(mesh, T)