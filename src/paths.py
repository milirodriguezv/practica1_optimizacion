import heapq
from itertools import permutations
import numpy as np
from src.board import cell_is_free


def evaluate_path(base, tasks, path, dist, speed=1.0, consumption=1.0, max_time=np.inf, max_energy=np.inf):
    """
    Evalúa una misión que comienza y termina en la base.
    """
    total_dist = 0.0
    time = 0.0
    energy = 0.0
    reward = 0.0

    # Inspección en cada punto visitado
    for task in path:
        reward += tasks[task, 2]
        time += tasks[task, 3]
        energy += tasks[task, 4]

    # Desplazamientos: base -> tareas -> base
    if path:
        points = [base] + [tasks[task, :2] for task in path] + [base]
        for a, b in zip(points[:-1], points[1:]):
            leg = dist(a, b)
            total_dist += leg
            time += leg / speed
            energy += leg * consumption

    feasible = bool(time <= max_time and energy <= max_energy)

    return {"reward": float(reward),
            "time": float(time),
            "energy": float(energy),
            "distance": float(total_dist),
            "feasible": feasible}


def feasible_paths(base, tasks, dist, speed=1.0, consumption=1.0, max_time=np.inf, max_energy=np.inf):
    """
    Enumera todas las rutas factibles sin repetir puntos. La ruta vacía también se incluye.
    """
    paths = []
    for n in range(len(tasks) + 1):
        for path in permutations(range(len(tasks)), n):
            path = list(path)
            result = evaluate_path(
                base, tasks, path, dist, speed=speed, consumption=consumption, max_time=max_time, max_energy=max_energy
            )
            if result["feasible"]:
                paths.append(
                    {
                        "path": path,
                        "reward": result["reward"],
                        "time": result["time"],
                        "energy": result["energy"],
                        "distance": result["distance"],
                    }
                )
    return paths


def nearest_neighbor(base, tasks, dist, speed=1.0, consumption=1.0, max_time=np.inf, max_energy=np.inf):
    """
    Construye una ruta voraz (greedy) basada en la distancia.
    En cada iteración añade el punto no visitado más cercano cuya incorporación mantenga factible la misión completa.
    """
    path = []
    position = base
    for _ in range(len(tasks)):
        candidates = [i for i in range(len(tasks)) if i not in path]
        candidates = sorted(candidates, key=lambda i: dist(position, tasks[i, :2]))
        for i in candidates:
            new_path = path + [i]
            result = evaluate_path(
                base, tasks, new_path, dist, speed=speed, consumption=consumption, max_time=max_time, max_energy=max_energy
            )
            if result["feasible"]:
                path.append(i)
                position = tasks[i, :2]
                break

    return path

def astar(start, end, walls, size, dist):
    """
    Busca un camino de coste mínimo entre dos celdas usando A*.
    Devuelve una lista de celdas desde inicio hasta objetivo, ambas incluidas. Devuelve None si no existe un camino.
    """
    pass


def mission_solver(
    base,
    tasks,
    walls,
    size,
    dist,
    planner=nearest_neighbor,
    pathfinder=astar,
    speed=1.0,
    consumption=1.0,
    max_time=np.inf,
    max_energy=np.inf,
):
    """
    Resuelve una misión completa: planifica la ruta y encuentra los caminos entre los puntos.
    Devuelve una lista de caminos, cada uno representado como una lista de celdas.
    """
    pass
