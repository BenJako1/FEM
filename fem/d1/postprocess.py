import matplotlib.pyplot as plt

def plot_temperature(mesh, T):
    plt.plot(mesh.x, T)
    plt.xlim(min(mesh.x), max(mesh.x))
    plt.grid()
    plt.xlabel("x")
    plt.ylabel("Temperature")
    plt.show()