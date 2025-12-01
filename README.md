# HeatFEM

HeatFEM is a lightweight finite element framework for solving steady-state heat
transfer problems in 1D, 2D, and 3D. It supports tetrahedral meshes, triangular
meshes, and line elements, and includes visualisation utilities.

## Installation

```bash
pip install git+https://github.com/BenJako1/HeatFEM.git
```

## Usage

A solver object is created using the HeatSolver class. Element type does not need to be specified as this is an ettribute of the mesh class.

```
from fem.solver import HeatSolver
sim = HeatSolver(mesh, ...)
```



