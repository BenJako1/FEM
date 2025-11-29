from fem.d3.solver import HeatSolver3D
from fem.d3.mesh import TetMesh3D

sim = HeatSolver3D(k=1)
sim.mesh = TetMesh3D(5, 3, 2, 6, 4, 3)

print(sim.mesh.elements)
print(sim.mesh.V)