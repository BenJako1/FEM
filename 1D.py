import numpy as np
import matplotlib.pyplot as plt

class Bar:
    def __init__(self, k, A):
        self.x = None
        self.N = None
        self.nodes = None
        self.elements = None

        self.k = k
        self.A = A
    
    def geometry(self, L=1, N=5, verbose=False):
        self.N = N
        self.nodes = np.array(list(range(N)))
        self.x = np.linspace(0, L, N)

        self.elements = np.zeros([N-1, 2])
        for i in range(len(self.elements)):
            self.elements[i, 0] = i
            self.elements[i, 1] = i+1

        if verbose:
            print(f'Nodes at: x={self.x}')
            print(f'Elements with nodes: \n {self.elements}')

    def assemble_conductance(self, verbose=False):
        element_conductance = np.array([[1, -1],
                                       [-1, 1]])
        self.Conductance = np.zeros([self.N, self.N])
        for i in range(self.N-1):
            coefficient = self.k * self.A / (self.x[i+1] - self.x[i])
            self.Conductance[i, i] += element_conductance[0, 0] * coefficient
            self.Conductance[i, i+1] += element_conductance[0, 1] * coefficient
            self.Conductance[i+1, i] += element_conductance[1, 0] * coefficient
            self.Conductance[i+1, i+1] += element_conductance[1, 1] * coefficient
        
        if verbose:
            print(f'Conductivity matrix: \n {self.Conductance}')
    
    def bound(self, boundDict, verbose=False):
        if len(set([len(boundDict["nodes"]), len(boundDict["type"]), len(boundDict["value"])])) != 1:
            raise ValueError("Boundary entries must have the same length")

        nodes_unpacked = []
        types_unpacked = []
        values_unpacked = []

        for node, type, value in zip(boundDict["nodes"], boundDict["type"], boundDict["value"]):
            if isinstance(node, str) and ":" in node:
                parts = [int(x) for x in node.split(":")]
                node_range = range(*parts)
                nodes_unpacked.extend(node_range)
                types_unpacked.extend([type] * len(node_range))
                values_unpacked.extend([value] * len(node_range))
            elif isinstance(node, (list, tuple)):
                nodes_unpacked.extend(node)
                types_unpacked.extend([type] * len(node))
                values_unpacked.extend([value] * len(node))
            else:
                nodes_unpacked.append(int(node))
                types_unpacked.append(type)
                values_unpacked.append(value)

        self.T = np.full(shape=[self.N], fill_value=None, dtype=object)
        self.Q = np.full(shape=[self.N], fill_value=0, dtype=object)
        self.boundNodes = []

        for i in range(len(nodes_unpacked)):
            if types_unpacked[i] == "temp":
                self.T[nodes_unpacked[i]] = values_unpacked[i]
                if self.Q[nodes_unpacked[i]] == 0:
                    self.Q[nodes_unpacked[i]] = None
                self.boundNodes.append(nodes_unpacked[i])
            elif types_unpacked[i] == "flux":
                self.Q[nodes_unpacked[i]] += values_unpacked[i]
            elif types_unpacked[i] == "gen":
                if self.Q[nodes_unpacked[i]] == None:
                    self.Q[nodes_unpacked[i]] = self.A * values_unpacked[i] * \
                                                    (self.x[nodes_unpacked[i]+1] - self.x[nodes_unpacked[i]]) / 2
                else:
                    self.Q[nodes_unpacked[i]] += self.A * values_unpacked[i] * \
                                                    (self.x[nodes_unpacked[i]+1] - self.x[nodes_unpacked[i]]) / 2
                if self.Q[nodes_unpacked[i]+1] == None:
                    self.Q[nodes_unpacked[i]+1] = self.A * values_unpacked[i] * \
                                                    (self.x[nodes_unpacked[i]+1] - self.x[nodes_unpacked[i]]) / 2
                else:
                    self.Q[nodes_unpacked[i]+1] += self.A * values_unpacked[i] * \
                                                (self.x[nodes_unpacked[i]+1] - self.x[nodes_unpacked[i]]) / 2
                
        self.freeNodes = [int(i) for i in range(self.N) if i not in self.boundNodes]

        if verbose:
            print(f'Temperature vector: {self.T}')
            print(f'Flux vector: {self.Q}')

    def solve(self):
        solutionArray = self.Conductance
        Q = self.Q

        for i in range(len(self.boundNodes)):
            solutionArray = np.delete(solutionArray, self.boundNodes[i] - i, axis=0)
            Q = np.delete(Q, self.boundNodes[i] - i, axis=0)
        
        for i in range(len(self.boundNodes)):
            Q = Q - solutionArray[:,self.boundNodes[i]] * self.T[self.boundNodes[i]]

        for i in range(len(self.boundNodes)):
            solutionArray = np.delete(solutionArray, self.boundNodes[i] - i, axis=1)

        if len(solutionArray[0]) >= 2:
            T_unknown = np.linalg.solve(np.float64(solutionArray), np.float64(Q))
        elif len(solutionArray[0]) == 1:
            T_unknown = np.array([Q[0] / solutionArray[0,0]])

        T_sol = np.zeros([self.N])
        for i in range(len(self.freeNodes)):
            T_sol[self.freeNodes[i]] = T_unknown[i]
        for i in range(len(self.boundNodes)):
            T_sol[self.boundNodes[i]] = self.T[self.boundNodes[i]]
        
        Q_sol = np.float64(self.Conductance) @ np.float64(T_sol)

        return T_sol, Q_sol

if __name__ == "__main__":
    sim = Bar(k=25, A=1)
    sim.geometry(L=1, N=5, verbose=False)
    sim.assemble_conductance(verbose=False)
    boundDict = {"nodes": [0, 4], "type": ["flux", "temp"], "value": [400,0]}
    sim.bound(boundDict, verbose=False)
    T, Q = sim.solve()

    print(T, Q)

    plt.plot(sim.x, T)
    plt.grid()
    plt.show()

"""
TO DO:
- Add convection BC
- Edge case check especially on back calculating Q
"""