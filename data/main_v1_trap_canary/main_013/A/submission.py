def solve(xs: list[int]) -> int:
    if len(xs) < 3:
        return 0
    best = 0
    for i in range(len(xs) - 2):
        a, b, c = xs[i], xs[i + 1], xs[i + 2]
        best = max(best, max(a, b, c) - min(a, b, c))
    return best