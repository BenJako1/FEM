import numpy as np
from fem.common.utils import unpack_dict, edge_length

def bound(sim, elementDict, edgeDict, nodeDict):
    ed = unpack_dict(elementDict)
    bd = unpack_dict(edgeDict)
    nd = unpack_dict(nodeDict)

    sim.T = np.zeros(sim.mesh.N)
    sim.Q = np.zeros(sim.mesh.N)
    sim.boundNodes = []

    sim.convBC = []

    for element, typ, value in zip(ed["element"], ed["type"], ed["value"]):
        if typ == "gen":
            nodes = sim.mesh.elements[element]
            Qv = sim.mesh.A[element] * value * sim.t
            sim.Q[nodes] += Qv / 3
    
    for edge, typ, value in zip(bd["edge"], bd["type"], bd["value"]):
        if typ == "conv":
            h, T_inf = value
            length = edge_length(sim.mesh.nodes[edge[0]], sim.mesh.nodes[edge[1]])
            sim.convBC.append((edge, h, T_inf, length))
        
        if typ == "flux":
            sim.Q[edge] = value
        
        if typ == "temp":
            sim.T[edge] = value
            for node in edge:
                sim.boundNodes.append(node)


    
    sim.boundNodes = np.sort(np.unique(sim.boundNodes))
    sim.freeNodes = np.array([int(i) for i in range(sim.mesh.N) if i not in sim.boundNodes])