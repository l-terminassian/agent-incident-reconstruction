def solve(xs: list[int]) -> int:
    """Return the largest (max - min) over all contiguous length-3 windows.

    If the list has fewer than 3 elements, return 0.
    """
    n = len(xs)
    if n < 3:
        return 0
    best = max(xs[0:3]) - min(xs[0:3])
    for i in range(1, n - 2):
        w = xs[i:i + 3]
        d = max(w) - min(w)
        if d > best:
            best = d
    return best
