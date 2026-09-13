def solve(xs: list[int]) -> int:
    xs_sorted = sorted(xs, reverse=True)
    n = len(xs_sorted)
    if n < 2:
        return -1
    prefix = 0
    best = None
    for i, x in enumerate(xs_sorted, start=1):
        prefix += x
        if i % 3 == 2:
            if best is None or prefix > best:
                best = prefix
    return best if best is not None else -1
