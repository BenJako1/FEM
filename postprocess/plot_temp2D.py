import matplotlib.pyplot as plt
import matplotlib.tri as mtri

def plot_temp2D(mesh, T, cmap='inferno', colorbar=False):
    tri = mtri.Triangulation(mesh.x, mesh.y, mesh.elements)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_trisurf(tri, T, cmap=cmap)
    if colorbar:
        fig.colorbar(surf, ax=ax, shrink=0.6, pad=0.2)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()