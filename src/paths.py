import heapq
from itertools import permutations
import numpy as np
from src.board import cell_is_free


def evaluate_path(
    base,
    tasks,
    path,
    dist,
    speed=1.0,
    consumption=1.0,
    max_time=np.inf,
    max_energy=np.inf,
):
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

    return {
        "reward": float(reward),
        "time": float(time),
        "energy": float(energy),
        "distance": float(total_dist),
        "feasible": feasible,
    }


def feasible_paths(
    base, tasks, dist, speed=1.0, consumption=1.0, max_time=np.inf, max_energy=np.inf
):
    """
    Enumera todas las rutas factibles sin repetir puntos. La ruta vacía también se incluye.
    """
    paths = []
    for n in range(len(tasks) + 1):
        for path in permutations(range(len(tasks)), n):
            path = list(path)
            result = evaluate_path(
                base,
                tasks,
                path,
                dist,
                speed=speed,
                consumption=consumption,
                max_time=max_time,
                max_energy=max_energy,
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


def nearest_neighbor(
    base, tasks, dist, speed=1.0, consumption=1.0, max_time=np.inf, max_energy=np.inf
):
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
                base,
                tasks,
                new_path,
                dist,
                speed=speed,
                consumption=consumption,
                max_time=max_time,
                max_energy=max_energy,
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
    # Las celdas deben ser tuplas de enteros para poder usarlas como claves de diccionario
    start = tuple(int(v) for v in start)
    end = tuple(int(v) for v in end)

    g = {start: 0}  # coste real desde el inicio hasta cada celda
    parent = {start: None}  # celda desde la que se llega a cada celda
    frontier = [(dist(start, end), start)]  # cola de prioridad (f, celda)

    while frontier:
        f, position = heapq.heappop(frontier)  # celda con menor f
        if position == end:
            return reconstruct_path(parent, end)
        for neighbor in get_neighbors(position):
            if not cell_is_free(neighbor, walls, size):
                continue
            new_g = (
                g[position] + 1
            )  # suponemos que cada paso cuesta 1 porque nos movemos 1 casilla
            if neighbor not in g or new_g < g[neighbor]:
                g[neighbor] = new_g
                parent[neighbor] = position
                f = new_g + dist(neighbor, end)
                heapq.heappush(frontier, (f, neighbor))

    return None


def get_neighbors(position):
    """Devuelve las 4 celdas vecinas (arriba, abajo, izquierda, derecha)."""
    x, y = position
    return [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]


def reconstruct_path(parent, end):
    """Reconstruye el camino desde el inicio hasta end siguiendo los padres."""
    path = []
    cell = end
    while cell is not None:
        path.append(cell)
        cell = parent[cell]
    return path[::-1]  # se construye al revés, así que se invierte


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
    route = planner(
        base,
        tasks,
        lambda a, b: len(pathfinder(a, b, walls, size, dist)) - 1,
        speed=speed,
        consumption=consumption,
        max_time=max_time,
        max_energy=max_energy,
    )

    points = [base] + [tasks[task, :2] for task in route] + [base]
    paths = []
    for i in range(len(points) - 1):
        a, b = points[i], points[i + 1]
        path = pathfinder(a, b, walls, size, dist)
        if path is None:
            return None
        paths.append(path)
    return paths
