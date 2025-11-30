from fem.d1.solver import HeatSolver1D
from fem.d1.mesh import LineMesh1D
import numpy as np

sim = HeatSolver1D(k=0.2, A=200)
sim.mesh = LineMesh1D(L=120, N=20)

print(len(sim.mesh.elements))

from fem.d2.solver import HeatSolver2D
from fem.d2.mesh import TriMesh2D
import numpy as np

sim = HeatSolver2D(k=600, t=0.1)
sim.mesh = TriMesh2D(120, 160, 20, 2)

print(len(sim.mesh.elements))