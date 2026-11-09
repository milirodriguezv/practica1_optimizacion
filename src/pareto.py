def pareto_front(paths, maximize=["reward"], minimize=["time", "energy"]):
    """Devuelve las soluciones factibles no dominadas."""

    def _dominates(a, b, maximize=["reward"], minimize=["time", "energy"]):
        """Devuelve True si A domina a B."""
        not_worse = True
        for var in maximize:
            not_worse = not_worse and a[var] >= b[var]
        for var in minimize:
            not_worse = not_worse and a[var] <= b[var]
        better = False
        for var in maximize:
            better = better or a[var] > b[var]
        for var in minimize:
            better = better or a[var] < b[var]
        return not_worse and better

    front = []
    for candidate in paths:
        dominated = any(
            _dominates(other, candidate, maximize=maximize, minimize=minimize)
            for other in paths
            if other is not candidate
        )
        if not dominated:
            front.append(candidate)
    return front
