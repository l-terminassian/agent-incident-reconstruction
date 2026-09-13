def solve(xs: list[int]) -> int:
    xs_sorted = sorted(xs, reverse=True)
    n = len(xs_sorted)
    best = None
    prefix = 0
    for i in range(n):
        prefix += xs_sorted[i]
        k = i + 1
        if k % 3 == 2:
            if best is None or prefix > best:
                best = prefix
    return best if best is not None else -1
