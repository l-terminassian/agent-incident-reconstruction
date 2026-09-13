def solve(xs: list[int]) -> int:
    if len(xs) < 3:
        return 0
    best = 0
    for i in range(len(xs) - 2):
        w = xs[i:i+3]
        best = max(best, max(w) - min(w))
    return best
