import numpy as np
from fem.common.utils import unpack_dict

def bound(sim, boundDict):
    bd = unpack_dict(boundDict)

    for node, typ, value in zip(bd["nodes"], bd["type"], bd["value"]):
        if typ == "temp":
            sim.T[node] = value
            sim.boundNodes.append(node)

        elif typ == "flux":
            sim.Q[node] += value

        elif typ == "gen":
            Qv = sim.A * value * sim.mesh.element_len[node]
            sim.Q[node] += Qv / 2
            sim.Q[node + 1] += Qv / 2

        elif typ == "convFace":
            h, Tinf = value
            sim.Q[node] += h * Tinf * sim.A
            sim.Convection[node] += h * sim.A

        elif typ == "convSurf":
            h, Wc, Tinf = value
            area = Wc * sim.mesh.element_len[node]

            sim.Q[node] += h * area * Tinf / 2
            sim.Q[node+1] += h * area * Tinf / 2

            sim.Convection[node] += h * area / 2
            sim.Convection[node+1] += h * area / 2

    sim.freeNodes = [i for i in range(sim.N) if i not in sim.boundNodes]