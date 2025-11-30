from fem.solver import HeatSolver
from fem.d2.mesh import TriMesh2D

mesh = TriMesh2D(120, 160, 100, 10)

sim = HeatSolver(mesh, k=0.2, t=1.25)

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

sim.boundary.apply_temp1d(wall, 330)
sim.boundary.apply_conv2d(sim.mesh.elements, 2e-4, 30)
sim.boundary.apply_conv1d(free, 2e-4, sim.t, 30)

#sim.boundary.apply_temp2d(wall, 330)
#sim.boundary.apply_conv2d(free, 2e-4, 30)
#sim.boundary.apply_conv2d(top, 2e-4, 30)
#sim.boundary.apply_conv2d(bottom, 2e-4, 30)

print("done assembling")
T, Q = sim.solve()
print("done solving")

from fem.d3.postprocess import visualise_tet_mesh
from fem.d2.postprocess import plot_surface
from fem.d1.postprocess import plot_temperature

plot_surface(mesh, T)