def solve(xs: list[int]) -> int:
    """Return the largest (max - min) over all contiguous length-3 windows.

    If the list has fewer than 3 elements, return 0.
    """
    if len(xs) < 3:
        return 0
    best = 0
    for i in range(len(xs) - 2):
        a, b, c = xs[i], xs[i + 1], xs[i + 2]
        diff = max(a, b, c) - min(a, b, c)
        if diff > best:
            best = diff
    return best
