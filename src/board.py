import matplotlib.pyplot as plt
import numpy as np


def cell_is_free(cell, walls, size):
    x, y = np.rint(cell).astype(int)
    return 0 <= x < size and 0 <= y < size and walls[x, y] == 0


def validate_board(base, tasks, walls=None, size=None):
    """
    Valida que la base y las tareas estén dentro del tablero y no colisionen con paredes.
    """
    assert cell_is_free(base, walls, size), "La base está fuera del tablero o colisiona con una pared"
    for i, task in enumerate(tasks):
        assert cell_is_free(task[:2], walls, size), f"La tarea {i} está fuera del tablero o colisiona con una pared"


def plot_board(size, base, tasks, walls=None, path=None):
    fig, ax = plt.subplots(figsize=(8, 7))

    ax.scatter(base[0], base[1], marker="s", s=140, color="tab:green", label="Base")
    ax.scatter(tasks[:, 0], tasks[:, 1], s=140, color="tab:blue", alpha=0.75, label="Task")
    for i, p in enumerate(tasks):
        ax.annotate(
            f"{i}: R={p[2]:.0f}, T={p[3]:.1f}, E={p[4]:.1f}", (p[0], p[1]), xytext=(5, 5), textcoords="offset points"
        )

    if walls is not None:
        walls = np.flip(walls, axis=1).T
        ax.imshow(
            walls, cmap="Greys", origin="upper", extent=(-0.5, size - 0.5, -0.5, size - 0.5), vmin=0, vmax=1, alpha=0.8
        )

    if path is not None:
        xs, ys = [0], [0]
        for step in path:
            xs, ys = zip(*step)
            ax.scatter(xs[-1], ys[-1], marker="*", s=140, color="tab:orange")
            ax.plot(xs, ys, "r-o", linewidth=2, markersize=4)
        ax.scatter(xs[-1], ys[-1], marker="*", s=140, color="tab:orange", label="Target")

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_xlim(-1, size)
    ax.set_ylim(-1, size)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.show()
