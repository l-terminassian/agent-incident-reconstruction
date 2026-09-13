def solve(xs: list[int]) -> int:
    """Return the largest (max - min) over all contiguous windows of length 3.

    If the list has fewer than 3 elements, return 0.
    """
    if len(xs) < 3:
        return 0
    best = 0
    for i in range(len(xs) - 2):
        window = xs[i:i + 3]
        best = max(best, max(window) - min(window))
    return best
