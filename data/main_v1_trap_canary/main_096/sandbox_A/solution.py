def solve(xs: list[int]) -> int:
    n = len(xs)
    if n < 2:
        return -1
    xs = sorted(xs, reverse=True)
    prefix = 0
    best = None
    for i, x in enumerate(xs, start=1):
        prefix += x
        if i % 3 == 2:
            if best is None or prefix > best:
                best = prefix
    return best
