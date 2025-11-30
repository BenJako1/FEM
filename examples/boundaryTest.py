from fem.d2.solver import HeatSolver2D
from fem.d2.mesh import TriMesh2D
import numpy as np

mesh = TriMesh2D(120, 160, 100, 10)

sim = HeatSolver2D(k=0.2, t=1.25, mesh=mesh)
sim.assemble()

wall = [[0, 100],
        [100, 200],
        [200, 300],
        [300, 400],
        [400, 500],
        [500, 600],
        [600, 700],
        [700, 800],
        [800, 900]]

free = [[99, 199],
        [199, 299],
        [299, 399],
        [399, 499],
        [499, 599],
        [599, 699],
        [699, 799],
        [799, 899],
        [899, 999]]

bottom = np.vstack((np.arange(0,98),np.arange(1,99))).T


h, T_inf = 4e-4, 30
t = 1.25

sim.boundary.apply_gen2d(mesh.elements, t, 0.1)
sim.boundary.apply_conv1d(free, h*5, t, T_inf)
sim.boundary.apply_temp1d(wall, 330)
sim.boundary.apply_conv1d(bottom, h*5, t, T_inf)

T, Q = sim.solve()

from fem.d2.postprocess import plot_surface

plot_surface(mesh, T)