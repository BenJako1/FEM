import numpy as np
from fem.common.utils import unpack_dict

def bound(sim, elementDict, nodeDict):
    sim.T = np.zeros(sim.mesh.N)
    sim.Q = np.zeros(sim.mesh.N)
    sim.boundNodes = []

    sim.convNodes = []
    sim.convElems = []

    ed = unpack_dict(elementDict)
    nd = unpack_dict(nodeDict)

    for element, typ, value in zip(ed["element"], ed["type"], ed["value"]):
        if typ == "gen":
            n1, n2 = sim.elements[element]
            Qv = sim.A * value * sim.mesh.element_len[element]
            sim.Q[n1] += Qv / 2
            sim.Q[n2] += Qv / 2

        elif typ == "convSurf":
            h, Wc, Tinf = value
            L = sim.mesh.element_len[element]
            area = Wc * L
            sim.convElems.append((element, h, Tinf, area))
    
    for node, typ, value in zip(nd["node"], nd["type"], nd["value"]):
        if typ == "temp":
            sim.T[node] = value
            sim.boundNodes.append(node)
        
        elif typ == "flux":
            sim.Q[node] += value
        
        elif typ == "convFace":
            h, Tinf = value
            area = sim.A
            sim.convNodes.append((node, h, Tinf, area))
    
    sim.freeNodes = [i for i in range(sim.mesh.N) if i not in sim.boundNodes]
    sim.convNodes = {entry[0]: (entry[1], entry[2], entry[3]) for entry in sim.convNodes}
    sim.convElems = {entry[0]: (entry[1], entry[2], entry[3]) for entry in sim.convElems}